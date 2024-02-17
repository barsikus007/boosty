import re
from collections.abc import Sequence
from struct import unpack
from typing import TYPE_CHECKING

from pydantic import BaseModel, HttpUrl

from boosty.types.base import ignore_missing_and_extra_fields
from boosty.types.media_types import Link, Text
from boosty.utils.json import json

if TYPE_CHECKING:
    from boosty.types import Content, Post
    from boosty.types.comment import Comment, CommentContent


# pyrogram/parser/utils.py:19@626a1bd
# SMP = Supplementary Multilingual Plane: https://en.wikipedia.org/wiki/Plane_(Unicode)#Overview
SMP_RE = re.compile(r"[\U00010000-\U0010FFFF]")


def add_surrogates(text):
    # Replace each SMP code point with a surrogate pair
    return SMP_RE.sub(
        lambda match:  # Split SMP in two surrogates
        "".join(chr(i) for i in unpack("<HH", match.group().encode("utf-16le"))),
        text,
    )
# pyrogram/parser/utils.py:41@626a1bd


class Entity(BaseModel):
    """Telegram-like entity"""

    type: str
    offset: int
    length: int
    url: str | None = None


def render_text(
        post_data: Sequence["Content | CommentContent"],
        *,
        header="", placeholder="\n\n",
        fix_long_newlines=True, fix_end_newlines=True,
) -> tuple[str, list[Entity]]:
    """
    :param post_data: any of boosty.types.media_types (types other than Text and Link will create placeholder)
    :param header: header for output text (for correct offsets)
    :param placeholder: placeholder for non-text content
    :param fix_long_newlines: remove 4+ newlines in a row
    :param fix_end_newlines: remove newlines at the end of text
    :return: tuple of text and list of entities (
    """
    text = header
    entities = []
    for content in post_data:
        while fix_long_newlines and text.endswith("\n\n\n\n"):
            text = text[:-1]
        if content.type in ["text", "link"]:
            content: Text | Link
            if isinstance(content, Text) and not ignore_missing_and_extra_fields:
                if content.modificator not in ["", "BLOCK_END"]:
                    raise ValueError(
                        f"TEXT PARSER ERROR\n"
                        f"content.modificator not in ['', 'BLOCK_END']\n"
                        f"{content}",
                    )
                if content.modificator == "BLOCK_END" and len(content.content):
                    raise ValueError(
                        f"TEXT PARSER ERROR\n"
                        f"content.modificator == 'BLOCK_END' with content!\n"
                        f"{content}",
                    )
            if len(content.content) == 0:
                if content.modificator == "BLOCK_END":
                    text += "\n"
                continue
            raw_text, raw_unstyled, raw_entities = json.loads(content.content)
            # pyrogram/parser/html.py:121@d53e1c2
            # raw_text = re.sub(r"^\s*(<[\w<>=\s\"]*>)\s*", r"\1", raw_text)
            # raw_text = re.sub(r"\s*(</[\w</>]*>)\s*$", r"\1", raw_text)
            if isinstance(content, Link):
                new_offset = len(add_surrogates(text.lstrip()))
                if len(text.lstrip()) == 0:
                    new_offset = new_offset - (len(raw_text) - len(raw_text.lstrip()))
                entities.append(Entity(
                    type="text_link", url=str(content.url),
                    offset=new_offset, length=len(add_surrogates(raw_text))))
            if raw_entities:
                if not ignore_missing_and_extra_fields and raw_unstyled != "unstyled":
                    raise ValueError(
                        f"TEXT PARSER ERROR\n"
                        f"raw_unstyled != 'unstyled'\n"
                        f"{raw_text, raw_unstyled, raw_entities =}",
                    )
                for format_list in raw_entities:
                    format_type, offset, length = format_list
                    if format_type == 0:
                        entity_type = "bold"
                    elif format_type == 2:
                        entity_type = "italic"
                    elif format_type == 4:
                        entity_type = "underline"
                    elif format_type is None:
                        continue  # TODO unknown format in comments [None, 64, 0]
                    else:
                        if not ignore_missing_and_extra_fields:
                            raise ValueError(
                                f"TEXT PARSER ERROR\n"
                                f"Unknown style\n"
                                f"{raw_text, raw_unstyled, raw_entities =}",
                            )
                        continue
                    new_offset = len(add_surrogates(text.lstrip())) + offset
                    if len(text.lstrip()) == 0:
                        new_offset = new_offset - (len(raw_text) - len(raw_text.lstrip()))
                    entities.append(Entity(type=entity_type, offset=new_offset, length=length))
            if len(text.lstrip()) == 0:
                raw_text = raw_text.lstrip()
            text += raw_text
        elif text:
            text.strip()
            text += placeholder

    while fix_end_newlines and text.endswith("\n"):
        text = text[:-1]
    return text, entities


def get_comment_url(post: "Post", comment: "Comment") -> HttpUrl:
    return HttpUrl(f"{post.url.query}{comment.query}")
