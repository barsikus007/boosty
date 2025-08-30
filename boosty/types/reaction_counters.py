from typing import Literal

from boosty.types.base import BaseObject

reaction_types = Literal[
    "angry",
    "applause",
    "banana",
    "blowing-up",
    "call-me",
    "check",
    "clown",
    "cold",
    "confetti",
    "crown",
    "cry",
    "diamond",
    "dislike",
    "eggplant",
    "fire",
    "folded-hands",
    "funny",
    "heart",
    "laught",
    "lightning",
    "like",
    "love",
    "melting",
    "money",
    "nausea",
    "peach",
    "pizza",
    "rocket",
    "sad",
    "scream",
    "splash",
    "swearing",
    "thinking",
    "wonder",
]

class ReactionCounters(BaseObject):
    type: reaction_types
    """Type of reaction. """
    count: int
    """Count of reaction type in post. """
