from __future__ import annotations

import typing as t

import httpx

from app.service_clients.retry_api_request_client import RetryApiRequestClient
from app.utils import CONFIG


class BaseAPIClient:
    """Base async HTTP API client using httpx. Subclasses set _host and optionally _timeout."""

    _timeout: float | int | None = CONFIG.config.get("INTERSERVICE_TIMEOUT")
    _host: str | None = None

    @classmethod
    def prepare_headers(cls, **extra: t.Any) -> dict[str, t.Any]:
        return {**extra}

    @classmethod
    def prepare_params(cls, **extra: t.Any) -> dict[str, t.Any]:
        return {**extra}

    @classmethod
    async def request(
        cls,
        method: str,
        path: str = "",
        *,
        params: dict[str, t.Any] | None = None,
        headers: dict[str, t.Any] | None = None,
        json: t.Any = None,
        content: t.Any = None,
        data: t.Any = None,
        files: t.Any = None,
        **kwargs: t.Any,
    ) -> httpx.Response:
        request_headers = cls.prepare_headers(**(headers or {}))
        request_params = cls.prepare_params(**(params or {}))
        base_url = getattr(cls, "_host", None) or ""
        timeout = getattr(cls, "_timeout", CONFIG.config.get("INTERSERVICE_TIMEOUT"))

        async with httpx.AsyncClient(base_url=base_url, timeout=timeout) as client:
            return await client.request(
                method,
                path,
                params=request_params,
                headers=request_headers,
                json=json,
                content=content,
                data=data,
                files=files,
                **kwargs,
            )

    @classmethod
    async def get(
        cls,
        path: str = "",
        *,
        params: dict[str, t.Any] | None = None,
        headers: dict[str, t.Any] | None = None,
        **kwargs: t.Any,
    ) -> httpx.Response:
        return await cls.request("GET", path, params=params, headers=headers, **kwargs)

    @classmethod
    async def post(
        cls,
        path: str = "",
        *,
        params: dict[str, t.Any] | None = None,
        headers: dict[str, t.Any] | None = None,
        json: t.Any = None,
        content: t.Any = None,
        data: t.Any = None,
        files: t.Any = None,
        **kwargs: t.Any,
    ) -> httpx.Response:
        return await cls.request(
            "POST",
            path,
            params=params,
            headers=headers,
            json=json,
            content=content,
            data=data,
            files=files,
            **kwargs,
        )

    @classmethod
    async def put(
        cls,
        path: str = "",
        *,
        params: dict[str, t.Any] | None = None,
        headers: dict[str, t.Any] | None = None,
        json: t.Any = None,
        content: t.Any = None,
        data: t.Any = None,
        files: t.Any = None,
        **kwargs: t.Any,
    ) -> httpx.Response:
        return await cls.request(
            "PUT",
            path,
            params=params,
            headers=headers,
            json=json,
            content=content,
            data=data,
            files=files,
            **kwargs,
        )

    @classmethod
    async def patch(
        cls,
        path: str = "",
        *,
        params: dict[str, t.Any] | None = None,
        headers: dict[str, t.Any] | None = None,
        json: t.Any = None,
        content: t.Any = None,
        data: t.Any = None,
        files: t.Any = None,
        **kwargs: t.Any,
    ) -> httpx.Response:
        return await cls.request(
            "PATCH",
            path,
            params=params,
            headers=headers,
            json=json,
            content=content,
            data=data,
            files=files,
            **kwargs,
        )

    @classmethod
    async def delete(
        cls,
        path: str = "",
        *,
        params: dict[str, t.Any] | None = None,
        headers: dict[str, t.Any] | None = None,
        **kwargs: t.Any,
    ) -> httpx.Response:
        return await cls.request("DELETE", path, params=params, headers=headers, **kwargs)

    @staticmethod
    def api_handler():
        def decorator(method: t.Callable[..., t.Coroutine[t.Any, t.Any, t.Any]]):
            async def wrapper(cls: type[BaseAPIClient], *args: t.Any, max_retries: int = 1, **kwargs: t.Any) -> t.Any:
                response = None
                with RetryApiRequestClient(max_retries=max_retries) as retry_manager:
                    response = await retry_manager.call_api(method, cls, *args, **kwargs)
                return response

            return wrapper

        return decorator
