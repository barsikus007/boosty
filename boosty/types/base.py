import os

from pydantic import BaseModel, Extra


schema_strict = bool(os.getenv("DEBUG"))


class BaseObject(BaseModel):
    class Config:
        extra = Extra.forbid if schema_strict else Extra.ignore
