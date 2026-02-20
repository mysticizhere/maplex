from __future__ import annotations
import typing as t

from app.constants import HttpStatusCodes


class BaseException(Exception):
    def __init__(
        self, 
        error: str,
        status_code: int = HttpStatusCodes.BAD_REQUEST.value, 
        meta: t.Any = None,
        quiet: bool = True,
        error_id: int | None = None,
        error_code: int | None = None,
        code: t.Any = None
    ) -> None:
        self._error = error
        self._status_code = status_code
        self._meta = meta
        self._quiet = quiet
        self._error_id = error_id
        self._error_code = error_code
        self._code = code

    @property
    def error(self) -> str:
        return self._error
    
    @property
    def status_code(self) -> int:
        return self._status_code
    
    @property
    def meta(self) -> t.Any:
        return self._meta
    
    @property
    def quiet(self) -> bool:
        return self._quiet
    
    @property
    def error_id(self) -> int | None:
        return self._error_id
    
    @property
    def error_code(self) -> int | None:
        return self._error_code
    
    @property
    def code(self) -> t.Any:
        return self._code

