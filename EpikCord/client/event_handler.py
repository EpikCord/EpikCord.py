from __future__ import annotations
import asyncio
from collections import defaultdict, deque
from logging import getLogger
from time import perf_counter_ns
from typing import Callable, DefaultDict, Deque, Dict, List, Optional, Union, TYPE_CHECKING

from discord_typings import GuildCreateEvent, GuildMemberUpdateEvent

from ..opcodes import GatewayOpcode
from .command_handler import CommandHandler

if TYPE_CHECKING:
    import discord_typings

logger = getLogger(__name__)





class EventHandler(CommandHandler):
    # Class that'll contain all methods that'll be called when an event is
    # triggered.

    def __init__(self):
        super().__init__()
        self.events: DefaultDict[str, List] = defaultdict(list)
        self.wait_for_events: DefaultDict[str, List] = defaultdict(list)
        self.latencies: Deque = deque(maxlen=5)

    def component(self, custom_id: str):
        """
        Execute this function when a component with the `custom_id` is interacted with.
        """

        def wrapper(func):
            self._components[custom_id] = func

        return wrapper

    async def handle_hello(self, event: discord_typings.HelloEvent):
        self.interval = event["d"]["heartbeat_interval"]

        async def wrapper():
            while True:
                await self.heartbeat(False)

        asyncio.create_task(wrapper())
        await self.identify()  # type: ignore

    def handle_heartbeat_ack(self, event: discord_typings.HeartbeatACKEvent):
        heartbeat_ack_time = perf_counter_ns()
        self.discord_latency: int = heartbeat_ack_time - self.heartbeat_time
        self.latencies.append(self.discord_latency)
        self.heartbeats.append(event["d"])

    async def handle_events(self):
        async for event in self.ws:
            event = event.json()
            logger.debug(f"Received {event} from Discord.")

            if event["op"] == GatewayOpcode.HELLO:
                await self.handle_hello()

            elif event["op"] == GatewayOpcode.DISPATCH:
                await self.handle_event(event)

            elif event["op"] == GatewayOpcode.HEARTBEAT:
                await self.heartbeat(True)

            elif event["op"] == GatewayOpcode.HEARTBEAT_ACK:
                self.handle_heartbeat_ack(event)

            elif event["op"] == GatewayOpcode.RECONNECT:
                await self.reconnect()

            elif event["op"] == GatewayOpcode.RESUMED:
                logger.debug(
                    "Connection successfully resumed and all proceeding events are new."
                )

        await self.handle_close()

    async def handle_event(self, event: dict):

        self.sequence = event["s"]

        results_from_event = event["d"]

        if hasattr(self, event["t"].lower()):
            try:
                await getattr(self, f"_{event['t'].lower()}")(results_from_event)  # type: ignore
            except Exception as e:
                logger.exception(f"Error handling event {event['t']}: {e}")
        else:
            logger.warning(
                f"EpikCord has no event handler for event {event['t']}, meaning that none of your event handlers are going to be called."
            )

    async def dispatch(self, event_name: str, *args, **kwargs):

        callbacks = self.events.get(event_name.lower())
        logger.info(f"Calling {len(callbacks)} for {event_name}")  # type: ignore

        for callback in callbacks:  # type: ignore
            await callback(*args, **kwargs)

        if not (wait_for_callbacks := self.wait_for_events.get(event_name.lower())):
            return

        for future, check in wait_for_callbacks:
            if check(*args):
                future.set_result(args)

    async def command_error(self, interaction, error: Exception):
        logger.exception(error)


__all__ = ("Event", "EventHandler")