from __future__ import annotations

import asyncio
import zlib
from collections import defaultdict
from functools import partial
from importlib.util import find_spec
from logging import getLogger
from sys import platform
from time import perf_counter_ns
from typing import TYPE_CHECKING, Any, DefaultDict, Dict, List, Optional, Union

import aiohttp
from discord_typings import HelloData, ReadyData

from ..exceptions import ClosedWebSocketConnection
from ..flags import Intents
from ..presence import Presence
from ..utils import AsyncFunction, GatewayCloseCode, IdentifyCommand, OpCode
from .rate_limit_tools import GatewayRateLimiter
from .ws_close_handler import (
    CloseHandlerLog,
    CloseHandlerRaise,
    close_dispatcher,
)

_ORJSON = find_spec("orjson")


if _ORJSON:
    import orjson as json
else:
    import json  # type: ignore

if TYPE_CHECKING:
    from .client import TokenStore
    from .http import HTTPClient

logger = getLogger("EpikCord.websocket")


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
        self.wait_for_events: DefaultDict[Union[str, int], List] = defaultdict(
            list
        )
        self.events: DefaultDict[str, List[AsyncFunction]] = defaultdict(list)
        self.opcode_mapping: Dict[OpCode, AsyncFunction] = {
            OpCode.HEARTBEAT: partial(self.heartbeat, forced=True),
            OpCode.RECONNECT: self.reconnect,
            OpCode.INVALID_SESSION: self.invalid_session,
            OpCode.HELLO: self.hello,
            OpCode.HEARTBEAT_ACK: self.heartbeat_ack,
        }

    def event(self):
        """Register an event handler. This is a decorator."""

        def decorator(func: AsyncFunction):
            name = func.__name__.lower().replace("on_", "")
            self.events[name].append(func)
            return func

        return decorator

    async def dispatch(self, event_name: str, *args, **kwargs):
        """Dispatch an event to all event handlers."""
        for event in self.events[event_name]:
            asyncio.create_task(event(*args, **kwargs))

    @staticmethod
    async def heartbeat_ack(_: Any):
        """Handle the heartbeat ack event. OpCode 11."""
        ...

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

        event = WaitForEvent(
            name=name, opcode=opcode, timeout=timeout, check=check
        )

        if opcode:
            self.wait_for_events[opcode.value].append(event)
        elif name:
            self.wait_for_events[name].append(event)

        return asyncio.wait_for(event.future, timeout=timeout)

    async def send_json(self, payload: Any):
        if not self.client.ws:
            logger.error(
                "Tried to send a payload without a websocket connection."
            )
            return
        await self.client.rate_limiter.tick()
        logger.debug("Sending %s to Gateway", payload)
        await self.client.ws.send_json(payload)

    async def _ready(self, data: ReadyData):
        self.client.session_id = data["session_id"]
        self.client.resume_url = data["resume_gateway_url"]

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

        async def heartbeat_task():
            while True:
                await self.heartbeat()

        asyncio.create_task(heartbeat_task())

    async def heartbeat(self, *, forced: Optional[bool] = False):
        """Send a heartbeat to the gateway.

        Parameters
        ----------
        forced : Optional[bool]
            Whether to send the heartbeat now.
        """

        if not self.client.heartbeat_interval:
            logger.error("Tried to send a heartbeat without an interval.")
            return

        if not forced:
            await asyncio.sleep(self.client.heartbeat_interval)

        await self.send_json({"op": OpCode.HEARTBEAT, "d": None})

        start = perf_counter_ns()

        await self.wait_for(
            opcode=OpCode.HEARTBEAT_ACK, timeout=self.client.heartbeat_interval
        )

        end = perf_counter_ns()

        self.client._heartbeats.append(end - start)

    async def resume(self):
        await self.send_json(
            {
                "op": OpCode.RESUME,
                "d": {
                    "seq": self.client.sequence,
                    "session_id": self.client.session_id,
                },
            }
        )

    async def reconnect(self, _):
        if self.client.ws:
            await self.client.ws.close()
        await self.client.connect()
        if self.client.session_id and self.client.sequence:
            await self.resume()

    async def resumed(self, _):
        logger.info(f"Resumed session {self.client.session_id}")

    async def invalid_session(self, resumable: bool):
        if self.client.ws:
            await self.client.ws.close()

        await self.client.connect()

        if resumable:
            await self.resume()
        else:
            await self.identify()

    async def handle(self, message: DiscordWSMessage):
        try:
            event = message.json()
        except json.JSONDecodeError:
            logger.error("Failed to decode message: %s", message.data)
            return

        values: List[Union[str, int]] = []

        if event["op"] in self.wait_for_events:
            values.append(event["op"])
        if event.get("t") and event["t"].lower() in self.wait_for_events:
            values.append(event["t"].lower())

        for value in values:
            for wait_for_event in self.wait_for_events[value]:
                if wait_for_event.check:
                    try:
                        await wait_for_event.check(event)
                    except Exception as exception:
                        wait_for_event.future.set_exception(exception)
                wait_for_event.future.set_result(event)
                self.wait_for_events[value].remove(wait_for_event)

        if event["op"] != OpCode.DISPATCH:
            await self.opcode_mapping[event["op"]](event["d"])
        else:
            await self.dispatch(
                event["t"].lower(), event["d"]
            )  # TODO: Once we have completed the HTTP objects, we can then start to transform them before they reach the end user.



class DiscordWSMessage:
    def __init__(self, *, data, msg_type, extra):
        self.data = data
        self.type = msg_type
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
            data=message, msg_type=ws_message.type, extra=ws_message.extra
        )

    async def close(self, *, code: int = 4000, message: bytes = b"") -> bool:
        logger.debug(
            "Closing websocket with code %s and message %s", code, message
        )
        return await super().close(code=code, message=message)


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
        self.event_handler: GatewayEventHandler = GatewayEventHandler(self)

        self.sequence: Optional[int] = None
        self.session_id: Optional[str] = None
        self.resume_url: Optional[str] = None
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
        asyncio.create_task(self.rate_limiter.reset.start())
        self.ws = await self.http.ws_connect(
            f"{url}?v={version}&encoding=json&compress=zlib-stream"
        )
        async for message in self.ws:
            logger.debug("Received message: %s", message.json())
            await self.event_handler.handle(message)  # type: ignore
        await self.handle_close()

    async def handle_close(self):
        if not self.ws:
            logger.debug("No websocket to handle close for.")
            return

        close_code = self.ws.close_code

        try:
            gce_code = GatewayCloseCode(close_code)
            ch_ins = close_dispatcher[gce_code]

        except (ValueError, KeyError) as e:
            raise ClosedWebSocketConnection(
                f"Connection has been closed with code {self.ws.close_code}"
            ) from e

        if isinstance(ch_ins, CloseHandlerRaise):
            raise ch_ins.exception(ch_ins.message)

        if isinstance(ch_ins, CloseHandlerLog):
            report_msg = "\n\nReport this immediately" * ch_ins.need_report
            logger.critical(ch_ins.message + report_msg)

        if ch_ins.resumable:
            await self.event_handler.resume()
