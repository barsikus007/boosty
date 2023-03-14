from typing import Annotated

from pydantic import Field

from .media_types import Text, Image


Teaser = Annotated[
    Text | Image,
    Field(discriminator="type")]
