from typing import Literal

from pydantic import HttpUrl, UUID4

from .base import BaseObject


player_urls_size_names = Literal[
    "ultra_hd",  # 2160
    "quad_hd",   # 1440
    "full_hd",   # 1080
    "high",      # 720
    "medium",    # 480
    "low",       # 360
    "lowest",    # 144
    "tiny",      # 144
]


class PlayerUrl(BaseObject):
    type: player_urls_size_names
    url: HttpUrl | Literal[""]


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
    title: str
    size: int


class Audio(FileBase):
    type: Literal["audio_file"]
    complete: bool
    title: str
    size: int

    """may be None if complete == False"""
    duration: int
    album: str
    artist: str
    track: str


class Video(FileBase):
    type: Literal["ok_video"]
    complete: bool
    """Unknown, probably True if video completely processed (could be False if Post.isRecord)"""
    title: str
    """Video title"""
    duration: int
    """Video duration in seconds"""
    width: int
    """Video max width in pixels"""
    height: int
    """Video max height in pixels"""
    playerUrls: list[PlayerUrl]
    """List of video urls for different resolutions"""
    defaultPreview: HttpUrl
    """random frame from video as thumbnail"""
    preview: HttpUrl
    """author thumbnail or defaultPreview"""
    previewId: UUID4 | None
    """author thumbnail image id or None"""
    vid: int
    """Unknown, probably ok.ru video id"""
    failoverHost: str
    """Unknown, probably interchangeable host for playerUrls"""


class Image(FileBase):
    type: Literal["image"]
    rendition: Literal["", "teaser_auto_background"]
    width: int | None
    """Could be None if redention=='teaser_auto_background' and """
    height: int | None
    """Could be None if redention=='teaser_auto_background'"""
