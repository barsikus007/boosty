# stolen from vkbottle with love <3
from __future__ import annotations

import json as json_module
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any, NotRequired, Self, TypedDict, Unpack

from aiohttp import ClientSession

if TYPE_CHECKING:
    from collections.abc import Mapping
    from types import TracebackType

    from aiohttp import ClientResponse
    from multidict import CIMultiDictProxy


class ABCHTTPClient(ABC):
    """Abstract class for http-clients
    Documentation: https://vkbottle.rtfd.io/ru/latest/low-level/http-client
    """

    json_processing_module: Any

    @abstractmethod
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        pass

    @abstractmethod
    async def request_raw(
        self,
        url: str,
        method: str = "GET",
        data: dict | None = None,
        **kwargs: Any,
    ) -> Any:
        pass

    @abstractmethod
    async def request_text(
        self,
        url: str,
        method: str = "GET",
        data: dict | None = None,
        **kwargs: Any,
    ) -> str:
        pass

    @abstractmethod
    async def request_json(
        self,
        url: str,
        method: str = "GET",
        data: dict | None = None,
        **kwargs: Any,
    ) -> dict:
        pass

    @abstractmethod
    async def request_content(
        self,
        url: str,
        method: str = "GET",
        data: dict | None = None,
        **kwargs: Any,
    ) -> bytes:
        pass

    @abstractmethod
    async def request_headers(
        self,
        url: str,
        data: dict | None = None,
        **kwargs: Any,
    ) -> Mapping[str, str]:
        pass

    @abstractmethod
    async def close(self) -> None:
        pass

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        await self.close()


class SessionParams(TypedDict):
    skip_auto_headers: NotRequired[set[str]]
    raise_for_status: NotRequired[bool]


class AiohttpClient(ABCHTTPClient):
    def __init__(
        self,
        session: ClientSession | None = None,
        json_processing_module: Any | None = None,
        *,
        optimize: bool = False,
        **session_params: Unpack[SessionParams],
    ) -> None:
        json_serialize = session_params.pop("json_serialize", None)
        self.json_processing_module = json_processing_module or json_serialize or json_module

        if optimize:
            session_params["skip_auto_headers"] = {"User-Agent"}
            session_params["raise_for_status"] = True

        self.session = session

        self._session_params = session_params

    async def request_raw(  # type: ignore[override]
        self,
        url: str,
        method: str = "GET",
        data: dict | None = None,
        **kwargs: Any,
    ) -> ClientResponse:
        if not self.session:
            self.session = ClientSession(  # type: ignore[misc]
                json_serialize=self.json_processing_module.dumps,
                **self._session_params,  # type: ignore[arg-type]
            )
        async with self.session.request(url=url, method=method, data=data, **kwargs) as response:
            await response.read()
            return response

    async def request_json(  # type: ignore[override]
        self,
        url: str,
        method: str = "GET",
        data: dict | None = None,
        **kwargs: Any,
    ) -> dict:
        response = await self.request_raw(url, method, data, **kwargs)
        return await response.json(
            encoding="utf-8",
            loads=self.json_processing_module.loads,
            content_type=None,
        )

    async def request_text(  # type: ignore[override]
        self,
        url: str,
        method: str = "GET",
        data: dict | None = None,
        **kwargs: Any,
    ) -> str:
        response = await self.request_raw(url, method, data, **kwargs)
        return await response.text(encoding="utf-8")

    async def request_content(  # type: ignore[override]
        self,
        url: str,
        method: str = "GET",
        data: dict | None = None,
        **kwargs: Any,
    ) -> bytes:
        response = await self.request_raw(url, method, data, **kwargs)
        return await response.read()

    async def request_headers(  # type: ignore[override]
        self,
        url: str,
        data: dict | None = None,
        **kwargs: Any,
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

    def __del__(self) -> None:
        if self.session and not self.session.closed:
            if self.session._connector is not None and self.session._connector_owner:
                self.session._connector._close()
            self.session._connector = None


class SingleAiohttpClient(AiohttpClient):
    __instance__ = None

    def __call__(self, *args: Any, **kwargs: Any):
        if self.__instance__ is None:
            self.__instance__ = super().__call__(*args, **kwargs)
        return self.__instance__
