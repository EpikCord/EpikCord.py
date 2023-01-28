from __future__ import annotations

import asyncio
from collections import defaultdict
from enum import IntEnum
from sys import platform
from time import perf_counter_ns
import zlib
from datetime import timedelta
from discord_typings import HelloData, IdentifyConnectionProperties
from importlib.util import find_spec
from typing import (
    Any,
    DefaultDict,
    Literal,
    Optional,
    TYPE_CHECKING,
    List,
    TypedDict,
    Union,
)
from typing_extensions import NotRequired
from logging import getLogger

import aiohttp

from ..ext import tasks
from ..flags import Intents
from ..presence import Presence, UpdatePresenceData
from ..utils import AsyncFunction

_ORJSON = find_spec("orjson")


if _ORJSON:
    import orjson as json
else:
    import json  # type: ignore

if TYPE_CHECKING:
    from .client import TokenStore
    from .http import HTTPClient

logger = getLogger("EpikCord.websocket")


class OpCode(IntEnum):
    DISPATCH = 0
    HEARTBEAT = 1
    IDENTIFY = 2
    STATUS_UPDATE = 3
    VOICE_STATE_UPDATE = 4
    VOICE_SERVER_PING = 5
    RESUME = 6
    RECONNECT = 7
    REQUEST_GUILD_MEMBERS = 8
    INVALID_SESSION = 9
    HELLO = 10
    HEARTBEAT_ACK = 11


class IdentifyData(TypedDict):
    token: str
    intents: int
    properties: IdentifyConnectionProperties
    compress: bool
    large_threshold: int
    presence: NotRequired[UpdatePresenceData]


class IdentifyCommand(TypedDict):
    op: Literal[OpCode.IDENTIFY]
    d: IdentifyData


class WaitForEvent:
    def __init__(
        self,
        *,
        name: Optional[str] = None,
        opcode: Optional[OpCode] = None,
        timeout: Optional[float] = None,
        check: Optional[AsyncFunction],
    ):
        self.event_name = name
        self.opcode = opcode
        self.timeout = timeout
        self.future: asyncio.Future = asyncio.Future()
        self.check = check


class GatewayEventHandler:
    def __init__(self, client: WebSocketClient):
        self.client = client
        self.wait_for_events: DefaultDict[Union[str, int], List] = defaultdict(list)

    def wait_for(
        self,
        *,
        name: Optional[str] = None,
        opcode: Optional[OpCode] = None,
        check: Optional[AsyncFunction] = None,
        timeout: Optional[float] = None,
    ):
        if not name and not opcode:
            raise ValueError("Either name or opcode must be provided.")
        elif name and opcode:
            raise ValueError("Only name or opcode can be provided.")

        event = WaitForEvent(name=name, timeout=timeout, check=check)

        if name:
            self.wait_for_events[name].append(event)
        elif opcode:
            self.wait_for_events[opcode.value].append(event)

        return asyncio.wait_for(event.future, timeout=timeout)

    async def send_json(self, payload: Any):
        if not self.client.ws:
            logger.error("Tried to send a payload without a websocket connection.")
            return
        await self.client.rate_limiter.tick()
        await self.client.ws.send_json(payload)

    async def identify(self):
        payload: IdentifyCommand = {
            "op": OpCode.IDENTIFY,
            "d": {
                "token": self.client.token.value,
                "intents": self.client.intents.value,
                "properties": {
                    "os": platform,
                    "browser": "EpikCord.py",
                    "device": "EpikCord.py",
                },
                "compress": True,
                "large_threshold": 50,
            },
        }

        if self.client.presence:
            payload["d"]["presence"] = self.client.presence.to_dict()

        await self.send_json(payload)

    async def hello(self, data: HelloData):
        """Handle the hello event. OpCode 10."""
        self.client.heartbeat_interval = data["heartbeat_interval"] / 1000
        await self.identify()

    async def heartbeat(self, *, forced: Optional[bool] = False):
        """Send a heartbeat to the gateway.

        Parameters
        ----------
        forced : Optional[bool]
            Whether or not to send the heartbeat now.
        """

        if not self.client.heartbeat_interval:
            logger.error("Tried to send a heartbeat without an interval.")
            return

        if not forced:
            await asyncio.sleep(self.client.heartbeat_interval)

        await self.send_json({"op": OpCode.HEARTBEAT, "d": None})

        start = perf_counter_ns()

        await self.wait_for(opcode=OpCode.HEARTBEAT_ACK, timeout=self.client.heartbeat_interval)

        end = perf_counter_ns()

        self.client._heartbeats.append(end - start)

    async def handle(self, message: DiscordWSMessage):
        try:
            event = message.json()
        except json.JSONDecodeError:
            logger.error("Failed to decode message: %s", message.data)
            return

        if event["op"] in self.wait_for_events:
            for event in self.wait_for_events[event["op"]]:
                if event.check:
                    try:
                        if await event.check(event):
                            event.future.set_result(event)
                    except Exception as exception:
                        event.future.set_exception(exception)
                else:
                    event.future.set_result(event)
        elif event["t"].lower() in self.wait_for_events:
            for event in self.wait_for_events[event["t"].lower()]:
                if event.check:
                    try:
                        if await event.check(event):
                            event.future.set_result(event)
                    except Exception as exception:
                        event.future.set_exception(exception)
                else:
                    event.future.set_result(event)

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
            self.buffer = bytearray()

        return DiscordWSMessage(
            data=message, type=ws_message.type, extra=ws_message.extra
        )


class WebSocketClient:
    def __init__(
        self,
        token: TokenStore,
        intents: Intents,
        *,
        presence: Optional[Presence] = None,
        http: HTTPClient,
    ):
        self.token: TokenStore = token
        self.intents: Intents = intents
        self.presence: Optional[Presence] = presence

        self.ws: Optional[GatewayWebSocket] = None
        self.http: HTTPClient = http

        self.rate_limiter: GatewayRateLimiter = GatewayRateLimiter()

        self.sequence: Optional[int] = None
        self.session_id: Optional[str] = None
        self.heartbeat_interval: Optional[float] = None
        self._heartbeats: List[int] = []

    @property
    def latency(self) -> Optional[float]:
        if not self._heartbeats:
            return None
        return sum(self._heartbeats) / len(self._heartbeats)

    async def connect(self):
        url = await self.http.get_gateway()
        version = self.http.version.value
        self.ws = await self.http.ws_connect(url, version=version)
