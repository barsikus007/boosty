from pydantic import conint, UUID4, BaseModel

from boosty.api.auth import Auth
from boosty.types import PostsResponse, Post, CommentsResponse
from boosty.utils.client import AiohttpClient


class Error(BaseModel):
    error: str
    error_description: str


class BoostyError(ValueError):
    pass


class API:
    API_URL = "https://api.boosty.to"
    DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    """https://techblog.willshouse.com/2012/01/03/most-common-user-agents/"""

    # TODO UserAPI
    # TODO AdminAPI
    def __init__(
            self,
            session: AiohttpClient = None,
            auth: Auth = None,
    ):
        self.session = session or AiohttpClient(base_url=self.API_URL)
        self.auth = auth or Auth()

    async def request(self, method: str, params: dict, data: dict = None) -> dict:
        if not params:
            params = {}
        if not data:
            data = {}
        params = {key: value for key, value in params.items() if value is not None}
        data = {key: value for key, value in data.items() if value is not None}
        response = await self.session.request_raw(
            method,
            method="GET",
            params=params,
            data=data,
            headers=self.auth.headers,
        )

        if response.status // 100 == 5:
            raise BoostyError(Error(error_description=str(response.status), error="Server error"))

        response_json = await response.json(
            encoding="utf-8", content_type=None
        )

        if response.status // 100 == 4:
            raise BoostyError(Error(**response_json))

        return response_json

    async def get_posts(
            self,
            name: str,

            limit: conint(ge=1, le=100) = None,  # limit is based on comments count
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
