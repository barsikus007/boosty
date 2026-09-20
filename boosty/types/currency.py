from typing import Literal
from boosty.types.base import BaseObject

currency_names = Literal["RUB", "USD", "EUR"]


class Currency(BaseObject):
    USD: int | float | dict
    RUB: int | float | dict
