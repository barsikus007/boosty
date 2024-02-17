from typing import Annotated, Literal

from pydantic import EmailStr, Field, HttpUrl

from .base import BaseObject


class BaseUser(BaseObject):
    id: int
    name: str
    # nick: str
    hasAvatar: bool
    avatarUrl: HttpUrl | Literal[""]
    isVerifiedStreamer: bool | None = None
    """None for BlogUser"""


class BlogUser(BaseUser):
    blogUrl: str
    flags: dict[Literal["showPostDonations"], bool] | None = None  # TODO


class Voter(BaseUser):
    # nickColor: conint(ge=0, le=15)
    """color id from 0 to 15"""
    # displayName: str
    vkplayProfileLink: HttpUrl | None = None


class DonatorUser(Voter):
    email: EmailStr | Literal[""]


class Commentator(BaseUser):
    nickColor: Annotated[int, Field(gt=0, le=15)] | None = None
    """color id from 0 to 15"""
    displayName: str | None = None
    vkplayProfileLink: HttpUrl | Literal[""] | None = None
