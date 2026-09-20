from typing import Literal
from boosty.types.base import BaseObject

currency_names = Literal["RUB", "USD", "EUR"]


class Currency(BaseObject):
    RUB: int | float
    USD: int | float | None = None
    """Absent in responses for blogs without foreign currency conversion"""
    EUR: int | float | None = None
    """Absent in responses for blogs without foreign currency conversion"""
