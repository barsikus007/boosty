from datetime import datetime
from typing import Literal

from pydantic import UUID4

from .base import BaseObject
from .users import Commentator
from .reactions import Reactions


class Reply(BaseObject):
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
    post: dict[Literal["id"], UUID4]
    data: list[dict]

    replyToUser: Commentator
    replyId: str
    parentId: str


class ReplyResponseExtra(BaseObject):
    isLast: bool
    isFirst: bool | None
    # TODO offset: int | None


class RepliesResponse(BaseObject):
    data: list[Reply]
    extra: ReplyResponseExtra
