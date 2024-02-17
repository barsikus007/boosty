# stolen from vkbottle with love <3
import asyncio
from abc import ABC, abstractmethod
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar

from aiohttp import ClientSession
from multidict import CIMultiDictProxy

from boosty.utils.json import json

if TYPE_CHECKING:
    from aiohttp import ClientResponse


TSingleAiohttpClient = TypeVar("TSingleAiohttpClient", bound="SingleAiohttpClient")


class ABCHTTPClient(ABC):
    """Abstract class for http-clients
    Documentation: https://github.com/vkbottle/vkbottle/blob/master/docs/low-level/http/http-client.md
    """

    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    async def request_raw(
        self, url: str, method: str = "GET", data: dict | None = None, **kwargs,
    ) -> Any:
        pass

    @abstractmethod
    async def request_text(
        self, url: str, method: str = "GET", data: dict | None = None, **kwargs,
    ) -> str:
        pass

    @abstractmethod
    async def request_json(
        self, url: str, method: str = "GET", data: dict | None = None, **kwargs,
    ) -> dict:
        pass

    @abstractmethod
    async def request_content(
        self, url: str, method: str = "GET", data: dict | None = None, **kwargs,
    ) -> bytes:
        pass

    @abstractmethod
    async def request_headers(
        self, url: str, data: dict | None = None, **kwargs,
    ) -> Mapping[str, str]:
        pass

    @abstractmethod
    async def open(self) -> None:
        pass

    @abstractmethod
    async def close(self) -> None:
        pass

    async def __aenter__(self) -> "ABCHTTPClient":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()


class AiohttpClient(ABCHTTPClient):
    def __init__(
        self,
        session: ClientSession | None = None,
        json_processing_module: Any | None = None,
        optimize: bool = False,
        **session_params,
    ):
        self.json_processing_module = (
            json_processing_module or session_params.pop("json_serialize", None) or json
        )

        if optimize:
            session_params["skip_auto_headers"] = {"User-Agent"}
            session_params["raise_for_status"] = True

        self.session = session

        self._session_params = session_params

    async def request_raw(
        self,
        url: str,
        method: str = "GET",
        data: dict | None = None,
        **kwargs,
    ) -> "ClientResponse":
        await self.open()
        try:
            async with self.session.request(url=url, method=method, data=data, **kwargs) as response:
                await response.read()
                return response
        except asyncio.TimeoutError as e:
            await self.close()
            self.session = None
            await self.open()
            raise asyncio.TimeoutError from e

    async def request_json(
        self,
        url: str,
        method: str = "GET",
        data: dict | None = None,
        **kwargs,
    ) -> dict:
        response = await self.request_raw(url, method, data, **kwargs)
        return await response.json(
            encoding="utf-8", loads=self.json_processing_module.loads, content_type=None,
        )

    async def request_text(
        self,
        url: str,
        method: str = "GET",
        data: dict | None = None,
        **kwargs,
    ) -> str:
        response = await self.request_raw(url, method, data, **kwargs)
        return await response.text(encoding="utf-8")

    async def request_content(
        self,
        url: str,
        method: str = "GET",
        data: dict | None = None,
        **kwargs,
    ) -> bytes:
        response = await self.request_raw(url, method, data, **kwargs)
        return response._body

    async def request_headers(
        self,
        url: str,
        data: dict | None = None,
        **kwargs,
    ) -> CIMultiDictProxy[str]:
        if not self.session:
            self.session = ClientSession(
                json_serialize=self.json_processing_module.dumps,
                **self._session_params,
            )
        async with self.session.head(url=url, data=data, **kwargs) as response:
            return response.headers

    async def open(self) -> None:
        if not self.session:
            self.session = ClientSession(
                json_serialize=self.json_processing_module.dumps,
                **self._session_params,
            )

    async def close(self) -> None:
        if self.session and not self.session.closed:
            await self.session.close()

    def __del__(self):
        if self.session and not self.session.closed:
            if self.session._connector is not None and self.session._connector_owner:
                self.session._connector.close()
            self.session._connector = None


class SingleAiohttpClient(AiohttpClient):
    __instance__ = None

    def __new__(
        cls: type[TSingleAiohttpClient], *args: Any, **kwargs: Any,
    ) -> TSingleAiohttpClient:
        if cls.__instance__ is None:
            cls.__instance__ = super().__new__(cls, *args, **kwargs)
        return cls.__instance__

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        pass  # no need to close session in this case
