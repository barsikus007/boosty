from typing import Annotated

from pydantic import Field

from .media_types import Image, TeaserAutoBackgroundImage, Text

ImageTeaser = Annotated[
    TeaserAutoBackgroundImage | Image,
    Field(discriminator="rendition")]


TeaserContent = Annotated[Text | ImageTeaser, Field(discriminator="type")]
