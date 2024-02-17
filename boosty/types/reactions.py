from typing import Literal

from .base import BaseObject

reaction_names = Literal[
    "heart",
    "like",
    "dislike",
    "laught",
    "wonder",
    "fire",
    "sad",
    "angry",
]


class Reactions(BaseObject):
    heart: int
    like: int
    dislike: int
    laught: int
    wonder: int
    fire: int
    sad: int
    angry: int


class Reacted(BaseObject):
    author: reaction_names
