# ruff: noqa: PLR0913
from http import HTTPStatus
from typing import Annotated, Literal

from pydantic import UUID4, BaseModel, Field

from boosty.api.auth import Auth
from boosty.types import Post, PostsResponse
from boosty.types.blacklist import BlacklistResponse
from boosty.types.comment import CommentsResponse
from boosty.types.deferred_access import DeferredAccess, DeferredAccessResponse, EditedDeferredAccess
from boosty.types.post import EditedPost, NewPost
from boosty.utils.client import ABCHTTPClient, SingleAiohttpClient
from boosty.utils.consts import API_URL
from boosty.utils.logging import logger


class Error(BaseModel):
    status_code: int
    error: str
    error_description: str | None = None


class BoostyError(Exception):
    pass


class API:
    def __init__(
        self,
        *,
        http_client: ABCHTTPClient | None = None,
        auth: Auth | None = None,
    ):
        self.http_client = SingleAiohttpClient() if http_client is None else http_client
        self.auth = Auth() if auth is None else auth

    async def request(self, method: str, path: str, params: dict | None = None, data: dict | None = None) -> dict:
        if not params:
            params = {}
        if not data:
            data = {}
        params = {key: value for key, value in params.items() if value is not None}
        data = {key: value for key, value in data.items() if value is not None}
        response = await self.http_client.request_raw(
            f"{API_URL}{path}",
            method=method,
            params=params,
            data=data,
            headers=self.auth.headers,
        )

        if response.status == HTTPStatus.UNAUTHORIZED:
            logger.warning("AUTH EXPIRED, REFRESHING VIA REFRESH_TOKEN...")
            await self.auth.refresh_auth_data(self.http_client, API_URL)
            return await self.request(method, path, params, data)

        try:
            response_json = await response.json(
                encoding="utf-8",
                content_type=None,
            )
        except ValueError as e:
            text = await response.text(errors="replace")
            if text.startswith("<html>\r\n<head><title>502 Bad Gateway</title></head>"):
                raise BoostyError(
                    Error(
                        status_code=response.status,
                        error="HTTPBadGateway",
                        error_description="Nginx 502 Bad Gateway",
                    ),
                ) from e
            if text.startswith("<html>\r\n<head><title>504 Gateway Time-out</title></head>"):
                raise BoostyError(
                    Error(
                        status_code=response.status,
                        error="HTTPGatewayTimeout",
                        error_description="Nginx 504 Gateway Time-out",
                    ),
                ) from e
            raise BoostyError(
                Error(
                    status_code=response.status,
                    error="Json decode error",
                    error_description=text,
                ),
            ) from e

        if not response.ok:
            raise BoostyError(
                Error(
                    status_code=response.status,
                    **response_json or {"error": "Unknown error"},
                ),
            )

        return response_json

    async def create_post(
        self,
        blog_name: str,
        *,
        new_post: NewPost,
    ) -> Post:
        resp_json = await self.request(
            "POST",
            f"/v1/blog/{blog_name}/post/",
            data=new_post.model_dump(),
        )
        return Post(**resp_json)

    async def get_posts(
        self,
        blog_name: str,
        *,
        limit: Annotated[int, Field(strict=True, ge=1, description="based on data amount (100 default)")] | None = None,
        offset: Annotated[str, Field(description="timestamp:idk,id?")] | None = None,
        comments_limit: Annotated[int, Field(strict=True, ge=0)] | None = None,
        reply_limit: int | None = None,  # idk ~1
        from_ts: int | None = None,
        to_ts: int | None = None,
        level_id: int | None = None,
        tags_ids: str | None = None,  # comma separated list of tags ids
    ) -> PostsResponse:
        resp_json = await self.request(
            "GET",
            f"/v1/blog/{blog_name}/post/",
            params={
                "limit": limit,
                "offset": offset,
                "comments_limit": comments_limit,
                "reply_limit": reply_limit,
                "from_ts": from_ts,
                "to_ts": to_ts,
                "level_id": level_id,
                "tags_ids": tags_ids,
            },
        )
        return PostsResponse(**resp_json)

    async def get_post(
        self,
        blog_name: str,
        post_id: UUID4 | str,
        *,
        comments_limit: Annotated[int, Field(strict=True, ge=0)] | None = None,
        reply_limit: int | None = None,  # idk ~1
    ) -> Post:
        resp_json = await self.request(
            "GET",
            f"/v1/blog/{blog_name}/post/{post_id}",
            params={
                "comments_limit": comments_limit,
                "reply_limit": reply_limit,
            },
        )
        return Post(**resp_json)

    async def update_post(
        self,
        blog_name: str,
        post_id: UUID4 | str,
        *,
        edited_post: EditedPost,
    ) -> Post:
        resp_json = await self.request(
            "PUT",
            f"/v1/blog/{blog_name}/post/{post_id}",
            data=edited_post.model_dump(),
        )
        return Post(**resp_json)

    async def delete_post(
        self,
        blog_name: str,
        post_id: UUID4 | str,
    ) -> Literal[True]:
        await self.request(
            "DELETE",
            f"/v1/blog/{blog_name}/post/{post_id}",
        )
        return True

    async def get_post_comments(
        self,
        blog_name: str,
        post_id: UUID4 | str,
        *,
        offset: str | None = None,  # "1654884900:923396"
        limit: Annotated[int, Field(strict=True, ge=0)] | None = None,  # ~20
        reply_limit: int | None = None,  # idk ~1
        order: str | None = None,  # ~"top"
    ) -> CommentsResponse:
        resp_json = await self.request(
            "GET",
            f"/v1/blog/{blog_name}/post/{post_id}/comment/",
            params={
                "offset": offset,
                "limit": limit,
                "reply_limit": reply_limit,
                "order": order,
            },
        )
        return CommentsResponse(**resp_json)

    async def get_post_deferred_access(
        self,
        blog_name: str,
        post_id: UUID4 | str,
    ) -> DeferredAccessResponse:
        resp_json = await self.request(
            "GET",
            f"/v1/blog/{blog_name}/post/{post_id}/deferred_access",
        )
        return DeferredAccessResponse(**resp_json)

    async def update_post_deferred_access(
        self,
        blog_name: str,
        post_id: UUID4 | str,
        *,
        edited_deferred_access: EditedDeferredAccess,
    ) -> DeferredAccess:
        resp_json = await self.request(
            "PUT",
            f"/v1/blog/{blog_name}/post/{post_id}/deferred_access",
            data=edited_deferred_access.model_dump(),
        )
        return DeferredAccess(**resp_json)

    async def get_blacklisted_users(
        self,
        *,
        blog_name: str,
    ) -> BlacklistResponse:
        resp_json = await self.request(
            "GET",
            "/v1/blacklist/",
            params={
                "blog_url": blog_name,
            },
        )
        return BlacklistResponse(**resp_json)
