from boosty.types.base import BaseObject
from boosty.types.users import BaseUser


class BlacklistedUser(BaseUser):
    blacklistedAt: int


class BlacklistResponse(BaseObject):
    data: list[BlacklistedUser]
