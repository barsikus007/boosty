from pydantic import UUID4, BaseModel, conint

from boosty.api.auth import Auth
from boosty.types import CommentsResponse, Post, PostsResponse
from boosty.utils.client import ABCHTTPClient, AiohttpClient
from boosty.utils.logging import logger


class Error(BaseModel):
    status_code: int
    error: str
    error_description: str | None = None


class BoostyError(Exception):
    pass


class API:
    API_URL = "https://api.boosty.to"

    def __init__(
            self,
            http_client: ABCHTTPClient = AiohttpClient(),
            auth: Auth = Auth(),
    ):
        self.http_client = http_client
        self.auth = auth

    async def request(self, method: str, params: dict, data: dict = None) -> dict:
        if not params:
            params = {}
        if not data:
            data = {}
        params = {key: value for key, value in params.items() if value is not None}
        data = {key: value for key, value in data.items() if value is not None}
        response = await self.http_client.request_raw(
            f"{self.API_URL}{method}",
            method="GET",
            params=params,
            data=data,
            headers=self.auth.headers,
        )

        if response.status == 401:
            logger.warning("AUTH EXPIRED, REFRESHING VIA REFRESH_TOKEN...")
            await self.auth.refresh_auth_data(self.http_client, self.API_URL)
            return await self.request(method, params, data)

        try:
            response_json = await response.json(
                encoding="utf-8", content_type=None,
            )
        except ValueError:
            response_json = {}

        if response.status // 100 != 2:
            raise BoostyError(
                Error(
                    status_code=response.status,
                    **response_json or {"error": "Unknown error"},
                ),
            )

        return response_json

    async def get_posts(
            self,
            name: str,
            *,
            limit: conint(ge=1) = None,  # limit is based on data amount ~300
            offset: str = None,  # "1654884900:923396"
            comments_limit: conint(ge=0) = None,
            reply_limit: int = None,  # idk ~1
    ) -> PostsResponse:
        resp_json = await self.request(
            f"/v1/blog/{name}/post/", params={
                "limit": limit,
                "offset": offset,
                "comments_limit": comments_limit,
                "reply_limit": reply_limit,
            })
        return PostsResponse(**resp_json)

    async def get_post(
            self,
            name: str,
            post_id: UUID4 | str,
            *,
            comments_limit: conint(ge=0) = None,
            reply_limit: int = None,  # idk ~1
    ) -> Post:
        resp_json = await self.request(
            f"/v1/blog/{name}/post/{post_id}", params={
                "comments_limit": comments_limit,
                "reply_limit": reply_limit,
            })
        return Post(**resp_json)

    async def get_post_comments(
            self,
            name: str,
            post_id: UUID4 | str,
            *,
            offset: str = None,  # "1654884900:923396"
            limit: conint(ge=0) = None,  # ~20
            reply_limit: int = None,  # idk ~1
            order: str = None,  # ~"top"
    ) -> CommentsResponse:
        resp_json = await self.request(
            f"/v1/blog/{name}/post/{post_id}/comment/", params={
                "offset": offset,
                "limit": limit,
                "reply_limit": reply_limit,
                "order": order,
            })
        return CommentsResponse(**resp_json)
