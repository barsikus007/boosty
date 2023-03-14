from datetime import datetime

from .base import BaseObject
from .users import DonatorUser


class Donator(BaseObject):
    id: int
    bloggerId: int
    targetId: int
    createdAt: datetime
    user: DonatorUser
    amount: int


class DonatorsResponseExtra(BaseObject):
    isLast: bool
    offset: int | None
    """Unknown, example: 10"""


class DonatorsResponse(BaseObject):
    data: list[Donator]
    extra: DonatorsResponseExtra
