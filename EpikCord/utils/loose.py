import asyncio
from importlib.util import find_spec
from logging import getLogger
from typing import Any, Dict

_ORJSON = find_spec("orjson")

if _ORJSON:
    import orjson as json
else:
    import json  # type: ignore

import aiohttp

logger = getLogger("EpikCord.utils")


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
    if url.startswith("/"):
        url = f"https://discord.com/api/v{version}{url}"
    else:
        url = f"https://discord.com/api/v{version}/{url}"

    if url.endswith("/"):
        url = url[:-1]

    return url


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
    tasks = {t for t in asyncio.all_tasks(loop=loop) if not t.done()}

    if not tasks:
        return

    for task in tasks:
        task.cancel()
    logger.debug(f"Cancelled {len(tasks)} tasks")
    loop.run_until_complete(asyncio.gather(*tasks, return_exceptions=True))


def cleanup_loop(loop) -> None:
    try:
        cancel_tasks(loop)
        logger.debug("Shutting down async generators.")
        loop.run_until_complete(loop.shutdown_asyncgens())
    finally:
        loop.close()
