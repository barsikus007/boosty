import logging
import os
from typing import Any, get_args

from pydantic import BaseModel, ConfigDict, model_validator

logger = logging.getLogger(__name__)


ignore_missing_and_extra_fields = os.getenv("IGNORE_MISSING_AND_EXTRA_FIELDS", "False").lower() in (
    "y",
    "yes",
    "t",
    "true",
    "1",
)

if ignore_missing_and_extra_fields:
    logger.warning("Ignoring missing and extra values")


def default_value_resolver(field_type: type | None):
    if field_type is None:
        return None
    if not (field_types := get_args(field_type)):
        return field_type()
    return field_types[0]()


class BaseObjectStrict(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )


class BaseObjectIgnore(BaseModel):
    @model_validator(mode="before")
    @classmethod
    def _ignore_field_without_value(cls, values: Any) -> dict:
        if not isinstance(values, dict):
            return values
        for field in cls.model_fields.items():
            if field[0] not in values and field[1].is_required():
                values.setdefault(field[0], default_value_resolver(cls.model_fields[field[0]].annotation))
        return values


# TODO type is 3.12?
# TODO set extra allow by default?
BaseObject: type[BaseModel] = BaseObjectIgnore if ignore_missing_and_extra_fields else BaseObjectStrict
