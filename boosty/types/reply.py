from datetime import datetime
from typing import Literal

from pydantic import UUID4

from boosty.types.base import BaseObject
from boosty.types.reaction_counters import ReactionCounters
from boosty.types.reactions import Reacted, Reactions
from boosty.types.users import Commentator


class Reply(BaseObject):
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
    post: dict[Literal["id"], UUID4]
    data: list[dict]
    reactionCounters: list[ReactionCounters]

    replyToUser: Commentator
    replyId: int
    parentId: int


class ReplyResponseExtra(BaseObject):
    isLast: bool
    isFirst: bool


class RepliesResponse(BaseObject):
    data: list[Reply]
    extra: ReplyResponseExtra
