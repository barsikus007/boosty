import html
from typing import Literal

from pydantic import HttpUrl

from boosty.api import API
from boosty.types import BaseObject
from boosty.types.media_types import Video
from boosty.utils.json import json

size_dict = {"ultra": 6, "quad": 5, "full": 4, "hd": 3, "sd": 2, "low": 1, "lowest": 0, "mobile": -1}
size_names = Literal[
    "mobile",  # 144
    "lowest",  # 240
    "low",     # 360
    "sd",      # 480
    "hd",      # 720
    "full",    # 1080
    "quad",    # 1440
    "ultra",   # 2160
]


class VideoSize(BaseObject):
    name: size_names
    url: HttpUrl
    seekSchema: Literal[3]
    disallowed: Literal[False]


async def get_video_sizes(
        api: API,
        name: str,
        content: Video
) -> list[VideoSize]:
    """
    :param api: API instance
    :param name: str for native referer header
    :param content: Video to get links from
    :return: list of VideoSize, sorted by quality descending
    """
    player_html = await api.session.request_text(
        content.url, headers={"User-Agent": api.auth.user_agent, "referer": f"https://boosty.to/{name}"})
    ind = player_html.find("data-options=")
    if ind == -1:
        raise ValueError("No data-options found in player script")
    do = ind + 14
    video_data_raw = html.unescape(player_html[do:player_html.find("\"", do)])
    video_data = json.loads(video_data_raw)

    sizes_list = json.loads(video_data["flashvars"]["metadata"])["videos"]
    sizes_list = [VideoSize(**size) for size in sizes_list]
    sizes_list.sort(key=lambda x: -size_dict[x.name])
    return sizes_list
