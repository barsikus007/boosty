from typing import Literal

from pydantic import UUID4

from boosty.types.base import BaseObject


class EditedDeferredAccess(BaseObject):
    isCommentsDenied: bool
    price: int
    applyTime: int


class DeferredAccess(EditedDeferredAccess):
    post: dict[Literal["id"], UUID4]


class DeferredAccessResponse(BaseObject):
    data: DeferredAccess
