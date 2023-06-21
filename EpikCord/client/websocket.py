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
from aiohttp import WSMsgType
from discord_typings import HelloEvent, InvalidSessionEvent, ReadyData

from ..exceptions import ClosedWebSocketConnection
from ..flags import Intents
from ..presence import Presence
from ..types import GatewayCloseCode, IdentifyCommand, OpCode
from ..utils import AsyncFunction
from .rate_limit_tools import GatewayRateLimiter
from .ws_close_handler import CloseHandlerLog, CloseHandlerRaise, close_dispatcher

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
        self.wait_for_events: DefaultDict[
            Union[str, int], List[WaitForEvent]
        ] = defaultdict(list)
        self.events: DefaultDict[str, List[AsyncFunction]] = defaultdict(list)
        self.opcode_mapping: Dict[OpCode, AsyncFunction] = {
            OpCode.HEARTBEAT: partial(self.heartbeat, forced=True),
            OpCode.RECONNECT: self.reconnect,
            OpCode.INVALID_SESSION: self.invalid_session,
            OpCode.HELLO: self.hello,
            OpCode.HEARTBEAT_ACK: self.heartbeat_ack,
            OpCode.DISPATCH: self._dispatch_event,
        }

    def event(self, func: AsyncFunction):
        """Register an event handler. This is a decorator."""

        name = func.__name__.lower().replace("on_", "")
        self.events[name].append(func)
        logger.info("Registered event %s", name)
        return func

    async def dispatch(self, event_name: str, *args, **kwargs):
        """Dispatch an event to all relevant event handlers."""
        for event in self.events[event_name]:
            asyncio.create_task(event(*args, **kwargs))

        logger.debug("Dispatched event %s", event_name)

    @staticmethod
    async def heartbeat_ack(_: Any):
        """Handle the heartbeat ack event (OPCODE 11)."""
        ...

    async def _dispatch_event(self, event: Dict[str, Any]):
        """Handle the DISPATCH event (OPCODE 0)."""
        event_name = event["t"].lower()
        event_data = event["d"]
        self.client.sequence = event["s"]

        if event_handler := getattr(self, f"_{event_name}", None):
            asyncio.create_task(event_handler(event_data))

        # TODO: Once we have completed the HTTP objects,
        #  we can then start to transform them before they reach
        #  the end user.

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

        event = WaitForEvent(name=name, opcode=opcode, timeout=timeout, check=check)

        if opcode:
            self.wait_for_events[opcode.value].append(event)
        elif name:
            self.wait_for_events[name].append(event)

        logger.debug("Waiting for event %s", name or opcode)

        return asyncio.wait_for(event.future, timeout=timeout)

    async def send_json(self, payload: Any):
        if not self.client.ws:
            logger.error("Tried to send a payload without a websocket connection.")
            return

        await self.client.rate_limiter.tick()

        logger.debug("Sending %s to Gateway", payload)

        for k, v in payload.items():
            if isinstance(v, OpCode):
                payload[k] = v.value
        await self.client.ws.send_json(payload)

    async def _ready(self, data: ReadyData):
        """Handle the READY dispatch event."""
        self.client.session_id = data["session_id"]
        self.client.resume_url = data["resume_gateway_url"]

        await self.dispatch("ready", data)

    async def _resumed(self, _: Any):
        """Handle the RESUMED dispatch event."""
        logger.info("Resumed session %s", self.client.session_id)
        await self.dispatch("resumed")

    async def identify(self):
        """Send the IDENTIFY payload to the Gateway (OPCODE 2)."""
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

    async def hello(self, event: HelloEvent):
        """Handle the hello event (OPCODE 10)."""

        data = event["d"]
        self.client.heartbeat_interval = data["heartbeat_interval"] / 1000

        if not self.client._resuming:
            await self.identify()
        else:
            await self.resume()

        if self.client._heartbeat_task:
            self.client._heartbeat_task.cancel()

        async def heartbeat_task():
            while True:
                await self.heartbeat()

        self.client._heartbeat_task = asyncio.create_task(heartbeat_task())

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

        await self.send_json({"op": OpCode.HEARTBEAT, "d": self.client.sequence})

        start = perf_counter_ns()
        try:
            await self.wait_for(
                opcode=OpCode.HEARTBEAT_ACK, timeout=self.client.heartbeat_interval
            )
        except asyncio.TimeoutError:
            logger.warning("Heartbeat ACK not received in time.")
            if self.client.ws:
                await self.client.ws.close(
                    client_triggered=True,
                    reason=(
                        "Heartbeat ACK not received in "
                        f"{self.client.heartbeat_interval}s."
                    ),
                )
            await self.client.connect(resume=True)
            return

        end = perf_counter_ns()

        self.client._heartbeats.append(end - start)

    async def resume(self):
        """Send the RESUME payload to the Gateway (OPCODE 6)."""
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
        """Handle the RECONNECT event (OPCODE 7)."""
        if self.client.ws:
            if self.client._heartbeat_task:
                self.client._heartbeat_task.cancel()
            await self.client.ws.close(
                client_triggered=True, reason="OpCode 7 was received."
            )
        await self.client.connect(resume=True)

    async def invalid_session(self, event: InvalidSessionEvent):
        """Handle the INVALID_SESSION event (OPCODE 9)."""
        resumable = event["d"]
        if self.client.ws:
            if self.client._heartbeat_task:
                self.client._heartbeat_task.cancel()
            await self.client.ws.close(
                client_triggered=True, reason="OpCode 9 was received."
            )

        await self.client.connect(resume=resumable)

    async def _handle_wait_for(self, event: Dict[str, Any]):
        """Set the Futures for wait_for events."""
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
                logger.debug("Set result for %s with data %s", value, event)
                self.wait_for_events[value].remove(wait_for_event)

    async def handle(self, message: DiscordWSMessage):
        try:
            event = message.json()
        except json.JSONDecodeError:
            logger.error("Failed to decode message: %s", message.data)
            return

        await self._handle_wait_for(event)

        await self.opcode_mapping[event["op"]](event)


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

    async def close(
        self,
        *,
        code: int = 4000,
        message: bytes = b"",
        client_triggered: bool = False,
        reason: str = "",
    ) -> bool:
        if self._closed:
            return False
        logger.debug(
            "Closing websocket with code %s and message %s. %s. %s",
            code,
            message,
            f"Client triggered: {client_triggered}" if client_triggered else "",
            f"Reason: {reason}" if reason else "",
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
        self._rate_limiter_task: Optional[asyncio.Task] = None

        self._gateway_url: Optional[str] = None

        self.sequence: Optional[int] = None
        self.session_id: Optional[str] = None
        self.resume_url: Optional[str] = None
        self.heartbeat_interval: Optional[float] = None
        self._heartbeats: List[int] = []
        self._heartbeat_task: Optional[asyncio.Task] = None
        self._resuming: bool = False

        self.event = self.event_handler.event

    @property
    def latency(self) -> Optional[float]:
        if not self._heartbeats:
            return None
        return sum(self._heartbeats) / len(self._heartbeats)

    async def connect(self, *, resume: bool = False):
        if not self._gateway_url and not resume:
            self._gateway_url = await self.http.get_gateway()

        self._resuming = resume

        version = self.http.version.value

        url = (
            f"{self._gateway_url if not resume else self.resume_url}"
            f"?v={version}&encoding=json&compress=zlib-stream"
        )

        if not self.resume_url and resume:
            raise ValueError("Cannot resume without a resume URL")
        elif not url:
            raise ValueError(f"Cannot connect to URL {url} (resume: {resume})")

        self.ws = await self.http.ws_connect(url)

        async def forever_reset():
            while True:
                await asyncio.sleep(60)
                await self.rate_limiter.reset()

        if self._rate_limiter_task:
            self._rate_limiter_task.cancel()
        self._rate_limiter_task = asyncio.create_task(forever_reset())
        async for message in self.ws:
            logger.debug(
                "Received message types: %s. Data: %s", message.type, message.json()
            )
            if message.type in (WSMsgType.BINARY, WSMsgType.TEXT):
                await self.event_handler.handle(message)  # type: ignore
            elif message.type in (
                WSMsgType.CLOSE,
                WSMsgType.CLOSED,
                WSMsgType.CLOSING,
                WSMsgType.ERROR,
            ):
                await self.handle_close()
                break

    async def handle_close(self):
        if not self.ws:
            logger.debug("No websocket to handle close for.")
            return

        close_code = self.ws.close_code
        if self._rate_limiter_task:
            self._rate_limiter_task.cancel()

        logger.critical("Websocket closed with code %s", close_code)

        if close_code in (
            GatewayCloseCode.NORMAL_CLOSURE,
            GatewayCloseCode.ABNORMAL_CLOSURE,
        ):
            await self.connect(resume=False)

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
            await self.connect(resume=True)
