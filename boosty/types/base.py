from pydantic import BaseModel, Extra


schema_strict = True  # TODO: make it configurable


class BaseObject(BaseModel):
    class Config:
        extra = Extra.forbid if schema_strict else Extra.ignore
