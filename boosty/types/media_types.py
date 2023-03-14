from typing import Literal

from pydantic import HttpUrl, UUID4

from .base import BaseObject


class PlayerUrls(BaseObject):
    # fullHD: str
    type: str | None  # TODO
    url: str | None  # TODO


class Text(BaseObject):
    type: Literal["text"]
    content: str
    modificator: str


class Smile(BaseObject):
    type: Literal["smile"]
    smallUrl: HttpUrl
    mediumUrl: HttpUrl
    largeUrl: HttpUrl
    name: str
    isAnimated: bool
    id: UUID4


class Link(BaseObject):
    type: Literal["link"]
    content: str
    url: HttpUrl
    explicit: bool


class LinkToVideo(BaseObject):
    type: Literal["video"]
    url: HttpUrl


class FileBase(BaseObject):
    id: UUID4
    url: HttpUrl


class File(FileBase):
    type: Literal["file"]
    complete: bool
    size: int
    title: str


class Audio(FileBase):
    type: Literal["audio_file"]
    complete: bool
    size: int
    title: str

    duration: int | None  # TODO
    album: str | None
    artist: str | None
    track: str | None


class Video(FileBase):
    type: Literal["ok_video"]
    complete: bool
    vid: str

    playerUrls: PlayerUrls | None
    title: str
    duration: int
    preview: str | None  # TODO
    failoverHost: str  # TODO

    width: int
    height: int
    defaultPreview: HttpUrl | str | None
    previewId: UUID4 | None


class Image(FileBase):
    type: Literal["image"]
    rendition: str
    """'' or 'teaser_auto_background'"""

    width: int | None
    """If redention=='teaser_auto_background', then value is None"""
    height: int | None
    """If redention=='teaser_auto_background', then value is None"""
