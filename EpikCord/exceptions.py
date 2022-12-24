from typing import Dict

import aiohttp

class EpikCordException(Exception):
    ...

class HTTPException(EpikCordException):
    def __init__(self, response: aiohttp.ClientResponse, data: Dict):
        ...

class NotFound(HTTPException):
    ...


class Forbidden(HTTPException):
    ...


class Unauthorized(HTTPException):
    ...


class BadRequest(HTTPException):
    ...