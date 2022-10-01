from __future__ import annotations
import asyncio
from collections import defaultdict, deque
from logging import getLogger
from time import perf_counter_ns
from typing import Callable, DefaultDict, Deque, Dict, Optional, Union, TYPE_CHECKING

from discord_typings import GuildCreateEvent, GuildMemberUpdateEvent

from ..opcodes import GatewayOpcode
from .command_handler import CommandHandler

if TYPE_CHECKING:
    import discord_typings

logger = getLogger(__name__)


class Event:
    def __init__(self, callback: Callable, *, event_name: str):
        self.callback = callback
        self.event_name = event_name or callback.__name__


class EventHandler(CommandHandler):
    # Class that'll contain all methods that'll be called when an event is
    # triggered.

    def __init__(self):
        super().__init__()
        self.events: DefaultDict = defaultdict(list)
        self.wait_for_events: DefaultDict = defaultdict(list)
        self.latencies: Deque = deque(maxlen=5)

    def wait_for(
        self,
        event_name: str,
        *,
        check: Optional[Callable] = None,
        timeout: Union[float, int] = 0,
    ):
        """
        Waits for the event to be triggered.

        Parameters
        ----------
        event_name : str
            The name of the event to wait for.
        check : Optional[callable]
            A check to run on the event.
            If it returns ``False``, the event will be ignored.
        timeout : int
            The amount of time to wait for the event.
            If not specified, it'll wait forever.
        """
        future: asyncio.Future = asyncio.Future()
        if not check:

            def check(*_, **__):
                return True

        self.wait_for_events[event_name.lower()].append((future, check))
        return asyncio.wait_for(future, timeout=timeout)

    def event(self, event_name: Optional[str] = None):
        def register_event(func):
            func_name = event_name or func.__name__.lower()

            if func_name.startswith("on_"):
                func_name = func_name[3:]

            self.events[func_name].append(func)

            return Event(func, event_name=func_name)

        return register_event

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

    async def _voice_server_update(self, data: discord_typings.VoiceServerUpdateEvent):
        voice_data: discord_typings.VoiceServerUpdateEvent = data["d"]
        payload = {
            "token": voice_data["token"],
            "endpoint": voice_data["endpoint"],
            "guild_id": voice_data["guild_id"],
        }

        if voice_data["endpoint"]:
            payload["endpoint"] = voice_data["endpoint"]

        return await self.dispatch("voice_server_update", payload)

    async def _voice_state_update(self, data: discord_typings.VoiceStateUpdateEvent):
        from EpikCord import VoiceState

        return await self.dispatch(
            "voice_state_update", VoiceState(self, data)
        )  # TODO: Make this return something like (VoiceState, Member) or make VoiceState get Member from member_id

    async def _guild_members_chunk(self, data: discord_typings.GuildMembersChunkEvent):
        ...

    async def _guild_delete(self, data: discord_typings.GuildDeleteEvent):
        guild = self.guilds.remove_from_cache(data["id"])  # type: ignore

        if guild:
            await self.dispatch("guild_delete", guild)

    async def _interaction_create(self, data: discord_typings.InteractionCreateEvent):
        interaction = self.utils.interaction_from_type(data)
        await self.handle_interaction(interaction)
        return interaction

    async def _channel_create(self, data: discord_typings.ChannelCreateEvent):
        channel = self.utils.channel_from_type(data)  # type: ignore
        self.channels.add_to_cache(channel.id, channel)  # type: ignore
        return channel

    async def _message_create(self, data: discord_typings.MessageCreateEvent):
        """Event fired when messages are created"""
        from EpikCord import Message

        message = Message(self, data)
        message.channel = self.channels.get(  # type: ignore
            message.channel_id
        ) or await self.channels.fetch(
            message.channel_id
        )  # type: ignore
        message.channel.last_message = message

        return message

    async def _guild_create(self, data: GuildCreateEvent):
        from EpikCord import Guild, Thread, UnavailableGuild

        if data.get("unavailable") is None:
            return  # TODO: Maybe a different event where the name says the Bot is removed on startup.

        guild = (
            UnavailableGuild(data)
            if data.get("unavailable") is True
            else Guild(self, data)
        )

        if not guild:
            return

        self.guilds.add_to_cache(guild.id, guild)

        for channel in data["channels"]:
            self.channels.add_to_cache(
                data["id"], self.utils.channel_from_type(channel)
            )

        for thread in data["threads"]:
            self.channels.add_to_cache(data["id"], Thread(self, thread))

        return guild

        # TODO: Add other attributes to cache

    async def _guild_member_update(self, data: GuildMemberUpdateEvent):
        from EpikCord import GuildMember

        guild_member = GuildMember(self, data)
        return self.members.get(data["id"]), guild_member

    async def _ready(self, data: discord_typings.ReadyEvent):
        from EpikCord import ClientApplication, ClientUser

        self.user: ClientUser = ClientUser(self, data["user"])
        self.session_id: Optional[str] = data["session_id"]
        application_response = await self.http.get("/oauth2/applications/@me")  # type: ignore
        application_data = await application_response.json()

        self.application = ClientApplication(self, application_data)

        if not self.overwrite_commands_on_ready:  # type: ignore
            return

        await self.utils.overwrite_commands()  # type: ignore
        await self.dispatch("ready")

    async def command_error(self, interaction, error: Exception):
        logger.exception(error)


__all__ = ("Event", "EventHandler")
