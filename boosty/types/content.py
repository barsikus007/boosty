from typing import Annotated

from pydantic import Field

from .media_types import Link, Text, LinkToVideo, File, Audio, Video, Image


Content = Annotated[
    Link | Text | LinkToVideo | File | Audio | Video | Image,
    Field(discriminator="type")]
