from datetime import datetime
from typing import Annotated, Literal

from pydantic import UUID4, Field

from boosty.types.base import BaseObject
from boosty.types.media_types import Image, Link, Smile, Text
from boosty.types.reactions import Reacted, Reactions
from boosty.types.reply import RepliesResponse
from boosty.types.users import Commentator
from boosty.utils.post import Entity, render_text

CommentContent = Annotated[
    Text | Smile | Image | Link,
    Field(discriminator="type")]


class Comment(BaseObject):
    id: UUID4
    intId: int
    createdAt: datetime
    updatedAt: datetime | None = None
    isBlocked: bool
    isUpdated: bool
    isDeleted: bool
    author: Commentator
    reactions: Reactions
    reacted: Reacted | None = None
    replyCount: int
    replies: RepliesResponse
    post: dict[Literal["id"], UUID4]
    data: list[CommentContent]

    @property
    def query(self) -> str:
        return f"?comment={self.intId}"

    @property
    def text(self) -> tuple[str, list[Entity]]:
        return render_text(self.data)


class CommentsResponseExtra(BaseObject):
    isLast: bool
    isFirst: bool | None = None


class CommentsResponse(BaseObject):
    data: list[Comment]
    extra: CommentsResponseExtra
