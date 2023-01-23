from __future__ import annotations

import asyncio
import zlib
from datetime import timedelta
from importlib.util import find_spec
from typing import Any, Optional, TYPE_CHECKING

import aiohttp

from ..presence import Presence
from ..ext import tasks
from ..flags import Intents

_ORJSON = find_spec("orjson")


if _ORJSON:
    import orjson as json
else:
    import json  # type: ignore

if TYPE_CHECKING:
    from .client import TokenStore
    from .http import HTTPClient

class GatewayRateLimiter:
    def __init__(self):

        self.event = asyncio.Event()
        self.event.set()

        self.remaining = 120
        self.limit = 120
        self.reset.run()

    @tasks.task(duration=timedelta(seconds=60))
    async def reset(self):
        self.remaining = self.limit
        self.event.set()

    async def tick(self):
        await self.event.wait()
        self.remaining -= 1
        if self.remaining == 0:
            self.event.clear()


class DiscordWSMessage:
    def __init__(self, *, data, type, extra):
        self.data = data
        self.type = type
        self.extra = extra

    def json(self) -> Any:
        return json.loads(self.data)


class GatewayWebSocket(aiohttp.ClientWebSocketResponse):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.buffer: bytearray = bytearray()
        self.inflator = zlib.decompressobj()

    async def receive(self, *args, **kwargs):
        ws_message = await super().receive(*args, **kwargs)
        message = ws_message.data

        if isinstance(message, bytes):

            self.buffer.extend(message)

            if len(message) < 4 or message[-4:] != b"\x00\x00\xff\xff":
                return

            message = self.inflator.decompress(self.buffer)

            message = message.decode("utf-8")
            self.buffer: bytearray = bytearray()

        return DiscordWSMessage(
            data=message, type=ws_message.type, extra=ws_message.extra
        )


class WebSocketClient:
    def __init__(self, token: TokenStore, intents: Intents, *, presence: Optional[Presence] = None, http: HTTPClient):
        self.token: TokenStore = token
        self.intents: Intents = intents
        self.presence: Optional[Presence] = presence

        self.ws: Optional[GatewayWebSocket] = None
        self.http: HTTPClient = http

        self.rate_limiter: GatewayRateLimiter = GatewayRateLimiter()

    async def connect(self):
        url = await self.http.get_gateway()
        