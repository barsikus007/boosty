from typing import Literal, Optional

from pydantic import HttpUrl, UUID4, root_validator

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
    "dash",                # TODO idk
    "dash_uni",            # TODO idk
    "hls",                 # TODO idk
    "tiny",                # TODO idk
    "live_hls",            # TODO idk
    "live_dash",           # TODO idk
    "live_playback_hls",   # TODO idk
    "live_playback_dash",  # TODO idk
]


class PlayerUrl(BaseObject):
    type: player_urls_size_names
    url: HttpUrl | Literal[""]


class Text(BaseObject):
    type: Literal["text"]
    content: str
    """JSON string with list of text with entities or '' if modificator is 'BLOCK_END'"""
    modificator: str
    """One of ['', 'BLOCK_END']"""


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

    uploadStatus: str  # TODO could be "ok" or other


class Video(FileBase):
    type: Literal["ok_video"]
    url: HttpUrl | Literal[""]
    """Could be '' due to boosty moment"""
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
    defaultPreview: HttpUrl | Literal[""]  # TODO SOMETIMES SERVER SENDS EMPTY STRING
    """random frame from video as thumbnail"""
    preview: HttpUrl | Literal[""]  # TODO SOMETIMES SERVER SENDS EMPTY STRING
    """author thumbnail or defaultPreview"""
    previewId: UUID4 | None = None
    """author thumbnail image id or None"""
    vid: int
    """Unknown, probably ok.ru video id"""
    failoverHost: str
    """Unknown, probably interchangeable host for playerUrls"""

    timeCode: int | None = None  # TODO
    viewsCounter: int | None = None  # TODO
    showViewsCounter: bool | None = None  # TODO
    uploadStatus: str  # TODO could be "ok" or other


class Image(FileBase):
    type: Literal["image"]
    rendition: Literal["", "teaser_auto_background"]
    width: Optional[int] = None
    height: Optional[int] = None

    @root_validator(pre=True)
    def check_width_height(cls, values):
        rendition, width, height = values.get('rendition'), values.get('width'), values.get('height')
        if rendition != 'teaser_auto_background':
            if width is None or height is None:
                raise ValueError('width and height must be provided unless rendition is "teaser_auto_background"')
        return values
