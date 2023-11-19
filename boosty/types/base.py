import os

from pydantic import BaseModel, Extra, ConfigDict

from boosty.utils.logging import logger

schema_strict = bool(os.getenv("DEBUG"))

if schema_strict:
    logger.warning("Schema strict mode is enabled")


class BaseObject(BaseModel):
    model_config = ConfigDict(
        extra=Extra.forbid if schema_strict else Extra.ignore,
    )
