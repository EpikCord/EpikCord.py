from dataclasses import dataclass
from typing import Dict

import aiohttp


class EpikCordException(Exception):
    ...

@dataclass
class LocatedError:
    code: str
    message: str
    path: str


class HTTPException(EpikCordException):
    def __init__(self, data: Dict):
        self.body = data
        self.code = data.get("code")
        self.message = data.get("message")
        self.errors = data.get("errors")
        self.errors_list = self.extract_errors(self.errors)

        super().__init__(
            "\n".join(f"{e.path} - {e.code} - {e.message}" for e in self.errors_list)
        )

    # def extract_errors(self, d, key_path=None):
    #     """Get _errors key from the given dictionary."""
    #     if key_path is None:
    #         key_path = []

    #     if d.get("_errors"):
    #         return [
    #             LocatedError(**error, path=".".join(key_path[1:]))
    #             for error in d.get("_errors", [])
    #         ]

    #     return [
    #         x
    #         for k, v in d.items()
    #         if isinstance(v, dict)
    #         for x in self.extract_errors(v, key_path + [k])
    #     ]

    def extract_errors(self, d, key_path=None):
        """Get _errors key from the given dictionary."""
        if key_path is None:
            key_path = []

        if d.get("_errors"):
            return [
                LocatedError(**error, path=".".join(f'{k}[{k}]' if isinstance(k, int) else k for k in key_path[1:]))
                for error in d.get("_errors", [])
            ]

        return [
            x
            for k, v in d.items()
            if isinstance(v, dict)
            for x in self.extract_errors(v, key_path + [k])
        ]


class NotFound(HTTPException):
    ...


class Forbidden(HTTPException):
    ...


class Unauthorized(HTTPException):
    ...


class BadRequest(HTTPException):
    ...


class TooManyRetries(EpikCordException):
    ...
