from enum import IntEnum, StrEnum


class HttpStatusCodes(IntEnum):
    SUCCESS = 200
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    REQUEST_TIMEOUT = 408
    INTERNAL_SERVER_ERROR = 500
    SERVICE_UNAVAILABLE = 503


class HttpMethods(StrEnum):
    GET = "get"
    POST = "post"
    PUT = "put"
    DELETE = "delete"
    PATCH = "patch"