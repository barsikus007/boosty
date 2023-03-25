import html
from typing import Literal

from pydantic import HttpUrl

from boosty.api import API
from boosty.types import BaseObject
from boosty.types.media_types import Video, PlayerUrl
from boosty.utils.json import json


player_size_dict = {
    "ultra_hd": 7,
    "quad_hd": 6,
    "full_hd": 5,
    "high": 3,
    "medium": 2,
    "low": 1,
    "lowest": 0,
    "tiny": -1,  # 4
}
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


class VideoSize(BaseObject):
    name: size_names
    url: HttpUrl
    seekSchema: Literal[3]
    disallowed: Literal[False]


async def get_video_sizes(
        api: API,
        name: str,
        content: Video,
) -> list[VideoSize]:
    """
    :param api: API instance
    :param name: str for native referer header
    :param content: Video to get links from
    :return: list of VideoSize, sorted by quality descending
    """
    player_html = await api.http_client.request_text(
        content.url, headers={"User-Agent": api.auth.user_agent, "referer": f"https://boosty.to/{name}"})
    ind = player_html.find("data-options=")
    if ind == -1:
        raise ValueError("No data-options found in player script")
    do = ind + 14
    video_data_raw = html.unescape(player_html[do:player_html.find("\"", do)])
    video_data = json.loads(video_data_raw)

    sizes_list = json.loads(video_data["flashvars"]["metadata"])["videos"]
    sizes_list = [VideoSize(**size) for size in sizes_list]
    return sorted(sizes_list, key=lambda x: -size_dict[x.name])


def sort_urls_by_quality(
        player_urls: list[PlayerUrl],
) -> list[PlayerUrl]:
    """
    :param player_urls: list of VideoSize, sorted randomly
    :return: list of VideoSize, sorted by quality descending
    """
    return sorted([_ for _ in player_urls if _.url != ""], key=lambda x: -player_size_dict[x.type])


async def select_max_size_url(
        api: API,
        player_urls: list[PlayerUrl],
        size_limit: int,
) -> tuple[PlayerUrl, str, int] | None:
    """
    :param api: API instance
    :param player_urls: PlayerUrls to filter
    :param size_limit: maximum size of video in bytes
    :return: best PlayerUrl possible
    """
    for player_url in sort_urls_by_quality(player_urls):
        # api.http_client.session.cookie_jar.clear()  # TODO enable if don't work
        resp = await api.http_client.session.head(player_url.url, headers=api.auth.headers)
        video_size = int(resp.headers["content-length"])
        if video_size < 228:
            raise ValueError("Video is too small, probably error code")
        if video_size <= size_limit:
            cd = resp.headers["content-disposition"]
            filename = cd[cd.find('"') + 1:cd.rfind('"')]
            return player_url, filename, video_size
