from typing import Literal

from pydantic import HttpUrl, EmailStr, conint

from .base import BaseObject


class BaseUser(BaseObject):
    id: int
    name: str
    nick: str
    hasAvatar: bool
    avatarUrl: HttpUrl | Literal[""]


class BlogUser(BaseUser):
    blogUrl: str


class DonatorUser(BaseUser):
    nickColor: conint(ge=0, le=15)
    """color id from 0 to 15"""
    displayName: str
    vkplayProfileLink: HttpUrl | None
    email: EmailStr
    isVerifiedStreamer: bool


class Commentator(BaseUser):
    nickColor: conint(ge=0, le=15)
    """color id from 0 to 15"""
    displayName: str
    vkplayProfileLink: HttpUrl | Literal[""]
