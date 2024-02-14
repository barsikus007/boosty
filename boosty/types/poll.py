from typing import Literal

from .base import BaseObject
from .users import Voter


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
    finishTime: int
    id: int
    title: list[str]
    options: list[Option]
    defaultLang: str
    hasOther: bool
    answer: list[int] | None = None
    other: Literal[""] | None = None
