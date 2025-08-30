from typing import Literal

from pydantic import UUID4

from boosty.types.base import BaseObject
from boosty.types.common import PostCommon
from boosty.types.reactions import Reacted, Reactions
from boosty.types.users import Commentator


class Reply(PostCommon):
    intId: int
    isUpdated: bool
    author: Commentator
    reactions: Reactions
    reacted: Reacted | None = None
    replyCount: int
    post: dict[Literal["id"], UUID4]
    data: list[dict]

    replyToUser: Commentator
    replyId: int
    parentId: int


class ReplyResponseExtra(BaseObject):
    isLast: bool
    isFirst: bool


class RepliesResponse(BaseObject):
    data: list[Reply]
    extra: ReplyResponseExtra
