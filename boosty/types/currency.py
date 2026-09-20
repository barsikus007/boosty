from typing import Literal
from boosty.types.base import BaseObject

currency_names = Literal["RUB", "USD", "EUR"]


class Currency(BaseObject):
    EUR: int | float
    USD: int | float
    RUB: int | float
