from typing import Annotated

from pydantic import Field

from .media_types import Audio, File, Image, Link, LinkToVideo, Text, Video

Content = Annotated[
    Link | Text | LinkToVideo | File | Audio | Video | Image,
    Field(discriminator="type")]
