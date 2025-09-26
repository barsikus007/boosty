from enum import IntEnum
from typing import Literal

from pydantic import UUID4, HttpUrl

from boosty.types.base import BaseObject

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
    "live_ondemand_hls",   # TODO idk
    "live_cmaf",           # TODO idk
]  # fmt: skip


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
    url: HttpUrl | Literal[""]


class File(FileBase):
    type: Literal["file"]
    complete: bool
    title: str
    size: int

    isMigrated: bool | None = None


class Audio(FileBase):
    type: Literal["audio_file"]
    complete: bool
    title: str
    size: int

    duration: int | None = None
    """Duration of audio track"""
    album: str | None = None
    """Album from MP3 ID3 Tag"""
    artist: str | None = None
    """Artist from MP3 ID3 Tag"""
    track: str | None = None
    """Track Name from MP3 ID3 Tag"""

    uploadStatus: str | None = None # TODO could be "ok" or other
    isMigrated: bool | None = None

    fileType: Literal["MP3", "WAV"] | None = None

    timeCode: int | None = None  # TODO
    viewsCounter: int | None = None  # TODO
    showViewsCounter: bool | None = None  # TODO


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
    uploadStatus: Literal["ok", "fail"] | None = None
    status: Literal["ok", "processing", "fail"]


class Image(FileBase):
    type: Literal["image"]
    rendition: Literal[""]
    width: int
    height: int
    size: int


class TeaserAutoBackgroundImage(FileBase):
    type: Literal["image"]
    rendition: Literal["teaser_auto_background"]
    width: int | None = None
    height: int | None = None
    size: int | None = None


class TextFormatEnum(IntEnum):
    bold = 0
    italic = 2
    underline = 4
