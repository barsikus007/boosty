from typing import Annotated, Literal, TypeAlias

from pydantic import EmailStr, Field, HttpUrl

from boosty.types.post import Currency
from boosty.types.base import BaseObject

UrlOrEmpty: TypeAlias = HttpUrl | Literal[""]


class BaseUser(BaseObject):
    id: int
    name: str
    isOfficial: bool | None = None  # is Official representor
    # nick: str
    hasAvatar: bool
    avatarUrl: UrlOrEmpty
    isVerifiedStreamer: bool | None = None
    """None for BlogUser"""
    currency: Currency
    """User currency"""


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
    vkplayProfileLink: UrlOrEmpty | None = None
