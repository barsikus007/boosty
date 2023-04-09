from typing import Literal, Annotated
from datetime import datetime

from pydantic import UUID4, Field

from .base import BaseObject
from .reply import RepliesResponse
from .users import Commentator
from .reactions import Reactions, Reacted
from .media_types import Text, Smile, Link, Image

CommentData = Annotated[
    Text | Smile | Image | Link,
    Field(discriminator="type")]


class Comment(BaseObject):
    id: UUID4
    intId: int
    createdAt: datetime
    updatedAt: datetime | None
    isBlocked: bool
    isUpdated: bool
    isDeleted: bool
    author: Commentator
    reactions: Reactions
    reacted: Reacted | None
    replyCount: int
    replies: RepliesResponse
    post: dict[Literal["id"], UUID4]
    data: list[CommentData]


class CommentsResponseExtra(BaseObject):
    isLast: bool
    isFirst: bool | None


class CommentsResponse(BaseObject):
    data: list[Comment]
    extra: CommentsResponseExtra
