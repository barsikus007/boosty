from datetime import datetime

from pydantic import UUID4

from boosty.types.base import BaseObject
from boosty.types.reaction_counters import ReactionCounters


class PostCommon(BaseObject):
    id: UUID4
    createdAt: datetime
    """Creation timestamp"""
    updatedAt: datetime | None = None
    """Last update timestamp (equal to createdAt at blog posts)"""

    isBlocked: bool
    """New option is Post Blocked by platform or some reason"""
    isDeleted: bool
    """TODO"""
    reactionCounters: list[ReactionCounters]
    """Another reaction counters, different from count.reactions (more reactions types)"""
