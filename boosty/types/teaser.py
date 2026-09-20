from typing import Annotated

from pydantic import Field

from boosty.types.media_types import Header, Image, Link, TeaserAutoBackgroundImage, Text

ImageTeaser = Annotated[TeaserAutoBackgroundImage | Image, Field(discriminator="rendition")]


TeaserContent = Annotated[Link | Text | Header | ImageTeaser, Field(discriminator="type")]
