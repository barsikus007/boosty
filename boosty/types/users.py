from typing import Literal

from pydantic import HttpUrl, EmailStr

from .base import BaseObject


class BlogUser(BaseObject):
    id: int
    name: str
    nick: str
    hasAvatar: bool
    avatarUrl: HttpUrl
    blogUrl: str


class DonatorUser(BaseObject):
    id: int
    name: str
    displayName: str
    nick: str
    hasAvatar: bool
    avatarUrl: HttpUrl | Literal[""]
    vkplayProfileLink: HttpUrl | None
    email: EmailStr


class Commentator(BaseObject):
    id: int
    name: str
    displayName: str
    nick: str
    hasAvatar: bool
    avatarUrl: HttpUrl | Literal[""]
    vkplayProfileLink: HttpUrl | Literal[""]
