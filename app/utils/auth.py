from __future__ import annotations

import functools
import hmac
import typing as t

from fastmcp.server.dependencies import get_http_headers

from app.exceptions.base_exception import BaseException
from app.utils import CONFIG
from app.constants import HttpStatusCodes


def _constant_time_compare(a: str, b: str) -> bool:
    return hmac.compare_digest(a.encode("utf-8"), b.encode("utf-8"))


def _get_expected_token(config_key: str = "AUTH_TOKEN") -> str | None:
    token = CONFIG.config.get(config_key)
    if token is None or (isinstance(token, str) and not token.strip()):
        return None
    return str(token).strip()


def require_bearer_token(config_key: str = "AUTH_TOKEN"):

    def decorator(fn: t.Callable[..., t.Awaitable[t.Any]]) -> t.Callable[..., t.Awaitable[t.Any]]:
        @functools.wraps(fn)
        async def wrapper(*args: t.Any, **kwargs: t.Any) -> t.Any:

            expected = _get_expected_token(config_key)
            if not expected:
                raise BaseException(
                    "Server auth not configured (missing AUTH_TOKEN in config)",
                    status_code=HttpStatusCodes.INTERNAL_SERVER_ERROR.value,
                )

            headers = get_http_headers()
            auth = headers.get("authorization") or headers.get("Authorization") or ""
            if not auth.startswith("Bearer "):
                raise BaseException(
                    "Missing or invalid Authorization header (expected Bearer token)",
                    status_code=HttpStatusCodes.UNAUTHORIZED.value,
                )
            token = auth[7:].strip()
            if not _constant_time_compare(token, expected):
                raise BaseException(
                    "Invalid token",
                    status_code=HttpStatusCodes.UNAUTHORIZED.value,
                )

            return await fn(*args, **kwargs)

        return wrapper

    return decorator
