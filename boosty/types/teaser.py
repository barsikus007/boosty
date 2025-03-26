from typing import Annotated

from pydantic import Field

from boosty.types.media_types import Image, Link, TeaserAutoBackgroundImage, Text

ImageTeaser = Annotated[TeaserAutoBackgroundImage | Image, Field(discriminator="rendition")]


TeaserContent = Annotated[Link | Text | ImageTeaser, Field(discriminator="type")]
