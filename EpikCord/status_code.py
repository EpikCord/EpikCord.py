from __future__ import annotations

from enum import IntEnum


class StatusCode(IntEnum):
    pass


class HTTPCodes(StatusCode):
    """HTTP response codes."""
    OK = 200
    CREATED = 201

    NO_CONTENT = 204
    NOT_MODIFIED = 304

    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405

    TOO_MANY_REQUESTS = 429

    GATEWAY_UNAVAILABLE = 502
    SERVER_ERROR = 500

    @classmethod
    def _missing_(cls, value: int) -> HTTPCodes:
        if (
            value > HTTPCodes.SERVER_ERROR
            and value != HTTPCodes.GATEWAY_UNAVAILABLE
        ):
            return HTTPCodes.SERVER_ERROR

        raise ValueError(
            f"HTTP Status Code `{value}` is undocumented.\n"
            "Please create an issue at: https://github.com/EpikCord/EpikCord.py/issues"
            " with the following traceback."
        )
