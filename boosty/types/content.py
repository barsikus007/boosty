from typing import Annotated

from pydantic import Field

from boosty.types.media_types import Audio, File, Header, Image, Link, LinkToVideo, Text, Video

Content = Annotated[
    Link | Text | Header | LinkToVideo | File | Audio | Video | Image,
    Field(discriminator="type")]
