import html
from typing import Literal

from pydantic import HttpUrl

from boosty.api import API
from boosty.types import BaseObject
from boosty.types.media_types import PlayerUrl, Video, player_urls_size_names
from boosty.utils.json import json

size_names = Literal[
    "ultra",   # 2160
    "quad",    # 1440
    "full",    # 1080
    "hd",      # 720
    "sd",      # 480
    "low",     # 360
    "lowest",  # 144
    "mobile",  # 144
]
size_dict = {
    "ultra": 7,
    "quad": 6,
    "full": 5,
    "hd": 3,
    "sd": 2,
    "low": 1,
    "lowest": 0,
    "mobile": -1,  # 4
}
player_size_dict = {
    "ultra_hd": 7,
    "quad_hd": 6,
    "full_hd": 5,
    "high": 3,
    "medium": 2,
    "low": 1,
    "lowest": 0,
    "dash": -1,
    "dash_uni": -2,
    "hls": -3,  # 4
    "tiny": -4,
    "live_playback_dash": -6,
    "live_playback_hls": -7,
    "live_dash": -8,
    "live_hls": -9,
}
player_size_by_number: dict[int, player_urls_size_names] = {v: k for k, v in player_size_dict.items()}  # type: ignore


class VideoSize(BaseObject):
    name: size_names
    url: HttpUrl
    seekSchema: Literal[3]
    disallowed: Literal[False]


async def get_video_sizes(
        api: API,
        name: str,
        content: Video,
) -> list[PlayerUrl]:
    """
    :param api: API instance
    :param name: str for native referer header
    :param content: Video to get links from
    :return: list of PlayerUrl, sorted by quality descending
    """
    player_html = await api.http_client.request_text(
        str(content.url), headers={"User-Agent": api.auth.user_agent, "referer": f"https://boosty.to/{name}"})
    ind = player_html.find("data-options=")
    if ind == -1:
        raise ValueError("No data-options found in player script")
    do = ind + 14
    video_data_raw = html.unescape(player_html[do:player_html.find('"', do)])
    video_data = json.loads(video_data_raw)

    sizes_list = json.loads(video_data["flashvars"]["metadata"])["videos"]
    sizes_list = [VideoSize(**size) for size in sizes_list]
    sizes_list = [
        PlayerUrl(url=size.url, type=player_size_by_number[size_dict[size.name]])
        for size in sizes_list]
    return sizes_list


def sort_urls_by_quality(
        player_urls: list[PlayerUrl],
) -> list[PlayerUrl]:
    """
    :param player_urls: list of PlayerUrl
    :return: list of PlayerUrl, sorted by quality descending
    """
    return sorted([_ for _ in player_urls if _.url != ""], key=lambda x: -player_size_dict[x.type])


async def select_max_size_url(
        api: API,
        player_urls: list[PlayerUrl],
        size_limit: int,
) -> tuple[PlayerUrl, str, int] | None:
    """
    :param api: API instance
    :param player_urls: list of PlayerUrl to filter
    :param size_limit: maximum size of video in bytes
    :return: best PlayerUrl possible
    """
    for player_url in sort_urls_by_quality(player_urls):
        headers = await api.http_client.request_headers(str(player_url.url), headers=api.auth.headers)
        video_size = int(headers["content-length"])
        if video_size < 228:
            raise ValueError("Video is too small, probably error code")
        if video_size <= size_limit:
            cd = headers["content-disposition"]
            filename = cd[cd.find('"') + 1:cd.rfind('"')]
            return PlayerUrl(url=player_url.url, type=player_url.type), filename, video_size
