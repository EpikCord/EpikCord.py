from dataclasses import dataclass
from typing import Dict


class EpikCordException(Exception):
    ...


@dataclass
class LocatedError:
    code: str
    message: str
    path: str


class HTTPException(EpikCordException):
    """Exception raised when the webserver throws error
    
    This inherits from :exc:`EpikcordException`.

    Parameters:
    ----------
    data: :class:`typing.Dict`


    Attributes
    ----------
    body: :class:`dict`
        
    code: :class:``
        The error code
    message: :class:``
        The message it returns
    errors: :class:`dict`
        The errors it returns
    errors_list: :class:`list`

    """
    def __init__(self, data: Dict):
        self.body = data
        self.code = data.get("code")
        self.message = data.get("message")
        self.errors = data.get("errors")
        self.errors_list = self.extract_errors(self.errors)

        super().__init__(
            "\n".join(
                f"{e.path} - {e.code} - {e.message}" for e in self.errors_list
            )
        )

    def extract_errors(self, d, key_path=None):
        """Get _errors key from the given dictionary."""
        if key_path is None:
            key_path = []

        if d.get("_errors"):
            return [
                LocatedError(
                    **error,
                    path=".".join(
                        f"{k}[{k}]" if isinstance(k, int) else k
                        for k in key_path[1:]
                    ),
                )
                for error in d.get("_errors", [])
            ]

        return [
            x
            for k, v in d.items()
            if isinstance(v, dict)
            for x in self.extract_errors(v, key_path + [k])
        ]


class NotFound(HTTPException):
    """Exception that's raised when status code 404 occurs.

    This inherits from :exc:`HTTPException`
    """
    ...


class Forbidden(HTTPException):
    """Exception that's raised when status code 403 occurs.

    This inherits from :exc:`HTTPException`
    """
    ...


class Unauthorized(HTTPException):
    """Exception raised due to unauthorized access 

    This inherits from :exc:`HTTPException`
    """
    ...


class BadRequest(HTTPException):
    """Exception raised due to

    This inherits from :exc:`HTTPException`
    """
    ...


class TooManyRetries(EpikCordException):
    """Exception raised due to constant retries

    This inherits from :exc:`EpikCordException`
    """
    ...


class ClosedWebSocketConnection(EpikCordException):
    """Exception raised due to

    This inherits from :exc:`EpikCordException`
    """
    ...


class DisallowedIntents(ClosedWebSocketConnection):
    """Exception raised due to

    This inherits from :exc:`EpikCordException`
    """
    ...


class InvalidIntents(ClosedWebSocketConnection):
    """Exception raised when an intent does not exist

    This inherits from :exc:`EpikCordException`
    """
    ...


class InvalidToken(ClosedWebSocketConnection):
    """Exception raised when fails to log you in from improper credentials

    This inherits from :exc:`EpikCordException`
    """
    ...


class GatewayRateLimited(ClosedWebSocketConnection):
    """Exception that's raised when status code 429 occurs
    and the timeout is greater than the configured maximum

    This inherits from :exc:`EpikCordException`
    """
    ...


class ShardingRequired(ClosedWebSocketConnection):
    """Exception raised due to

    This inherits from :exc:`EpikCordException`
    """
    ...


class UnknownMimeType(EpikCordException):
    """Exception raised due to
    
    This inherits from :exc:`EpikCordException`
    
    Parameters:
    ----------
    filename: :class:``
        The name of the file
    
    Attributes:
    ----------
    filename: :class:``
        The name of the file
    message: :class:`str`
        The message raised by error
    """
    def __init__(self, filename):
        self.filename = filename
        self.message = f"Cannot resolve mime type for file `{filename}`."
