from typing import Literal

from boosty.types.base import BaseObject
from boosty.types.users import Voter


class VotersResponseExtra(BaseObject):
    isLast: bool
    offset: int


class VotersResponse(BaseObject):
    data: dict[Literal["voters"], list[Voter]]
    extra: VotersResponseExtra


class Option(BaseObject):
    fraction: float
    counter: int
    id: int
    text: str
    voters: VotersResponse


class Poll(BaseObject):
    isMultiple: bool
    counter: int
    isFinished: bool
    finishTime: int | None = None
    id: int
    title: list[str]
    options: list[Option]
    defaultLang: str
    hasOther: bool
    answer: list[int] | None = None
    other: Literal[""] | None = None
