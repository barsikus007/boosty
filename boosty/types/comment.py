from typing import Literal, Annotated
from datetime import datetime

from pydantic import UUID4, Field

from .base import BaseObject
from .reply import RepliesResponse
from .users import Commentator
from .reactions import Reactions
from .media_types import Text, Smile, Image


CommentData = Annotated[
    Text | Smile | Image,
    Field(discriminator="type")]


class Smile(BaseObject):
    type: Literal["smile"]


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
    replyCount: int
    replies: RepliesResponse
    post: dict[Literal["id"], UUID4]
    data: list[CommentData]


class CommentsResponseExtra(BaseObject):
    isLast: bool
    isFirst: bool | None
    # TODO offset: int | None


class CommentsResponse(BaseObject):
    data: list[Comment]
    extra: CommentsResponseExtra
