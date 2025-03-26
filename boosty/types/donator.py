from datetime import datetime

from boosty.types.base import BaseObject
from boosty.types.users import DonatorUser


class Donator(BaseObject):
    id: int
    bloggerId: int
    targetId: int
    createdAt: datetime
    user: DonatorUser
    amount: float

    type: str  # TODO
    isFeePaid: bool  # TODO


class DonatorsResponseExtra(BaseObject):
    isLast: bool
    offset: int | None = None
    """Unknown, example: 10"""


class DonatorsResponse(BaseObject):
    data: list[Donator]
    extra: DonatorsResponseExtra
