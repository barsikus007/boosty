from typing import Literal

from pydantic import HttpUrl, EmailStr, conint

from .base import BaseObject


class BaseUser(BaseObject):
    id: int
    name: str
    nick: str
    hasAvatar: bool
    avatarUrl: HttpUrl | Literal[""]
    isVerifiedStreamer: bool | None
    """None for BlogUser"""


class BlogUser(BaseUser):
    blogUrl: str


class Voter(BaseUser):
    nickColor: conint(ge=0, le=15)
    """color id from 0 to 15"""
    displayName: str
    vkplayProfileLink: HttpUrl | None


class DonatorUser(Voter):
    email: EmailStr | Literal[""]


class Commentator(BaseUser):
    nickColor: conint(ge=0, le=15)
    """color id from 0 to 15"""
    displayName: str
    vkplayProfileLink: HttpUrl | Literal[""]
