from typing import Annotated

from pydantic import Field

from .media_types import Link, Image, TeaserAutoBackgroundImage, Text

ImageTeaser = Annotated[
    TeaserAutoBackgroundImage | Image,
    Field(discriminator="rendition")]


TeaserContent = Annotated[Link | Text | ImageTeaser, Field(discriminator="type")]
