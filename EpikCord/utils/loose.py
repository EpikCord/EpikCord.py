from __future__ import annotations

import asyncio
from functools import partial
from importlib.util import find_spec
from logging import getLogger
from types import ModuleType
from typing import TYPE_CHECKING, Any, Dict, Optional, Type, TypeVar

import aiohttp

from ..file import File

T = TypeVar("T")


_ORJSON = find_spec("orjson")
json: ModuleType

if _ORJSON:
    import orjson

    json = orjson

else:
    import json as _json

    json = _json

if TYPE_CHECKING:
    from . import SendingAttachmentData


def clear_none_values(d: dict):
    """
    Clears all the values in a dictionary that are None.
    """
    return {k: v for k, v in d.items() if v is not None}


def json_serialize(data, *args, **kwargs):
    return (
        json.dumps(data).decode("utf-8")  # type: ignore
        if _ORJSON
        else json.dumps(data)
    )


def clean_url(url: str, version: int) -> str:
    clean_uri: str = url.strip("/")
    return f"https://discord.com/api/v{version}/{clean_uri}"


async def extract_content(response: aiohttp.ClientResponse) -> Dict[str, Any]:
    if response.headers["Content-Type"] != "application/json":
        return {}
    data = await response.json()
    return data


def singleton(cls):
    instance = None

    def wrapper(*args, **kwargs):
        nonlocal instance

        if instance is None:
            instance = cls(*args, **kwargs)
        return instance

    return wrapper


def cancel_tasks(loop) -> None:
    logger = getLogger("EpikCord.cleanup")
    tasks = {t for t in asyncio.all_tasks(loop=loop) if not t.done()}

    if not tasks:
        return

    for task in tasks:
        task.cancel()
    logger.debug(f"Cancelled {len(tasks)} tasks")
    loop.run_until_complete(asyncio.gather(*tasks, return_exceptions=True))


def cleanup_loop(loop) -> None:
    logger = getLogger("EpikCord.cleanup")
    try:
        cancel_tasks(loop)
        logger.debug("Shutting down async generators.")
        loop.run_until_complete(loop.shutdown_asyncgens())
    finally:
        loop.close()


async def log_request(res, body: Optional[dict] = None):
    """Logs information about the request."""
    logger = getLogger("EpikCord.http")
    messages = [
        f"Sent a {res.method} to {res.url} "
        f"and got a {res.status} response. ",
        f"Content-Type: {res.headers['Content-Type']} ",
    ]

    if body:
        messages.append(f"Sent body: {body} ")

    if h := dict(res.request_info.headers):
        messages.append(f"Sent headers: {h} ")

    if h := dict(res.headers):
        messages.append(f"Received headers: {h} ")

    try:
        messages.append(f"Received body: {await res.json()} ")

    finally:
        logger.debug("".join(messages))


def add_file(
    form: aiohttp.FormData, file: File, i: int
) -> SendingAttachmentData:
    form.add_field(
        f"files[{i}]",
        file.contents,
        filename=file.filename,
        content_type=file.mime_type,
    )

    attachment: SendingAttachmentData = {
        "filename": file.filename,
        "id": i,
    }
    if file.description:
        attachment["description"] = file.description

    return attachment


def instance_or_none(cls: Type[T], value: Optional[Any]) -> Optional[T]:
    if value is not None:
        return None
    else:
        return cls(value)


int_or_none = partial(instance_or_none, cls=int)
