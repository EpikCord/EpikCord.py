from __future__ import annotations

import asyncio
from collections import defaultdict, deque
from logging import getLogger
from sys import platform
from time import perf_counter
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Coroutine,
    DefaultDict,
    Deque,
    Dict,
    List,
    Optional,
    Union,
)

from EpikCord.managers import ChannelManager, GuildManager

from ..close_event_codes import GatewayCECode
from ..close_handler import CloseHandlerLog, CloseHandlerRaise, close_dispatcher
from ..exceptions import ClosedWebSocketConnection
from ..ext.tasks import task
from ..flags import Intents
from ..opcodes import GatewayOpcode
from ..ws_events import setup_ws_event_handler
from .client_application import ClientApplication
from .client_user import ClientUser
from .http_client import HTTPClient

if TYPE_CHECKING:
    import discord_typings

    from EpikCord import Presence

    from .http_client import GatewayWebsocket

logger = getLogger(__name__)

Callback = Callable[..., Coroutine[Any, Any, Any]]


class Event:
    def __init__(self, callback: Callback, *, event_name: str):
        self.callback = callback
        self.event_name = event_name or callback.__name__


class GatewayRateLimiter:
    def __init__(self):

        self.event = asyncio.Event()
        self.event.set()

        self.remaining = 120
        self.limit = 120
        self.reset.run()

    @task(seconds=60)
    async def reset(self):
        self.remaining = self.limit
        self.event.set()

    async def tick(self):
        await self.event.wait()
        self.remaining -= 1
        if self.remaining == 0:
            self.event.clear()


class WebsocketClient:
    def __init__(
        self,
        token: str,
        intents: Union[Intents, int],
        presence: Optional[Presence] = None,
        discord_endpoint: str = "https://discord.com/api/v10",
    ):
        from EpikCord import Intents, Utils

        self.token = token
        if not token:
            raise TypeError("Missing token.")

        if isinstance(intents, int):
            self.intents = Intents(intents)
        elif isinstance(intents, Intents):
            self.intents = intents

        self._closed = True
        self.presence = presence

        self.http: HTTPClient = HTTPClient(token, discord_endpoint=discord_endpoint)

        self.events: DefaultDict[str, List[Callback]] = defaultdict(list)
        self.wait_for_events: DefaultDict[str, List] = defaultdict(list)

        self.heartbeats: Deque = deque(maxlen=10)
        self.heartbeat_interval: Optional[float] = None
        self.session_id: Optional[str] = None
        self.sequence: Optional[int] = None
        self.gateway_url: Optional[str] = None
        self.resume_gateway_url: Optional[str] = None
        self.websocket: Optional[GatewayWebsocket] = None

        self.utils = Utils(self)

        self.guilds: GuildManager = GuildManager(self)
        self.channels: ChannelManager = ChannelManager(self)

        self.user: Optional[ClientUser] = None
        self.application: Optional[ClientApplication] = None

        self.websocket_ratelimiter: Optional[GatewayRateLimiter] = None
        self.wse_handler = setup_ws_event_handler(self)
        self.latencies: Deque = deque(maxlen=10)

    @property
    def latency(self) -> Optional[int]:
        if not self.latencies:
            return None
        return sum(self.latencies) / len(self.latencies)

    async def heartbeat(self, forced: bool = False):
        if not self.heartbeat_interval:
            logger.critical("Cannot heartbeat without an interval.")
            return
        if not self.websocket:
            logger.critical("Cannot heartbeat without a websocket.")
            return

        if forced:
            await self.send_json(
                {
                    "op": GatewayOpcode.HEARTBEAT,
                    "d": self.sequence,
                }
            )
            return

        await asyncio.sleep(self.heartbeat_interval)
        await self.send_json(
            {
                "op": GatewayOpcode.HEARTBEAT,
                "d": self.sequence,
            }
        )

        start = perf_counter()
        async for event in self.websocket:
            if event.json()["op"] == GatewayOpcode.HEARTBEAT_ACK:
                end = perf_counter()
                break
        self.latencies.append(end - start)

    async def handle_ws_event(self, event_data):
        raw_op_code = event_data["op"]

        try:
            op_code = GatewayOpcode(raw_op_code)
        except ValueError:
            logger.critical("Unknown op code: %s", raw_op_code)
            return

        handler = self.wse_handler.get(op_code)
        await handler(event_data)

    async def connect(self, reconnect: bool = False):
        url = None

        if reconnect:
            url = self.resume_gateway_url
        else:
            if not self.gateway_url:
                self.gateway_url = url = (await self.http.get_gateway())["url"]

        logger.info("Connecting to gateway...")
        self.websocket = await self.http.ws_connect(  # type: ignore
            f"{url}?v=10&encoding=json"
        )
        logger.info("Connected to gateway! Listening to events!")
        self.websocket_ratelimiter = GatewayRateLimiter()
        self._closed = False

        async for event in self.websocket:  # type: ignore
            event_data = event.json()
            logger.debug(
                f"Received {event_data} from the Websocket Connection to Discord."
            )
            await self.handle_ws_event(event_data)

    async def reconnect(self):
        await self.close()
        await self.connect()

    async def resume(self):
        await self.send_json(
            {
                "op": GatewayOpcode.RESUME,
                "d": {
                    "token": self.token,
                    "session_id": self.session_id,
                    "seq": self.sequence,
                },
            }
        )

    async def handle_event(self, event_name: str, data: Dict):
        if hasattr(self, f"_{event_name}"):
            await getattr(self, f"_{event_name}")(data)

        for wait_for_callback in self.wait_for_events[event_name]:

            try:
                check_results = await wait_for_callback[1](data)
            except Exception:  # TODO: use a more specific exception
                return

            if check_results:
                wait_for_callback[0].set_result(data)
                self.wait_for_events[event_name].remove(wait_for_callback)

    async def dispatch(self, event_name: str, *args: Any, **kwargs: Any):
        for callback in self.events[event_name]:
            await callback(*args, **kwargs)
        logger.info(
            f"Dispatched {event_name} to {len(self.events[event_name])} listeners."
        )

    def wait_for(
        self,
        event_name: str,
        *,
        check: Optional[Callback] = None,
        timeout: float = 0,
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

            async def check(*_, **__):
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

    async def handle_close(self):
        close_code = self.websocket.close_code

        try:
            gce_code = GatewayCECode(close_code)
            ch_ins = close_dispatcher[gce_code]

        except (ValueError, KeyError) as e:
            raise ClosedWebSocketConnection(
                f"Connection has been closed with code {self.websocket.close_code}"
            ) from e

        if isinstance(ch_ins, CloseHandlerRaise):
            raise ch_ins.exception(ch_ins.message)

        if isinstance(ch_ins, CloseHandlerLog):
            report_msg = "\n\nReport this immediately" * ch_ins.need_report
            logger.critical(ch_ins.message + report_msg)

        if ch_ins.resumable:
            await self.resume()

    async def send_json(self, json: dict):

        if not self.websocket:
            logger.critical(f"Attempted to send {json} to Discord before connecting.")
            return

        if not self.websocket_ratelimiter:
            self.websocket_ratelimiter = GatewayRateLimiter()

        await self.websocket_ratelimiter.tick()
        await self.websocket.send_json(json)

        logger.debug(f"Sent {json} to the Websocket Connection to Discord.")

    async def close(self) -> None:
        if self._closed:
            return

        if self.websocket is not None and not self.websocket.closed:
            await self.websocket.close(code=4000)

        self._closed = True

    async def identify(self):
        await self.send_json(
            {
                "op": GatewayOpcode.IDENTIFY,
                "d": {
                    "token": self.token,
                    "intents": self.intents.value,
                    "properties": {
                        "os": platform,
                        "browser": "EpikCord.py",
                        "device": "EpikCord.py",
                    },
                },
            }
        )

    def login(self):
        loop = asyncio.get_event_loop()

        async def runner():
            try:
                await self.connect()
            finally:
                if not self._closed:
                    await self.close()

        def stop_loop_on_completion(f: asyncio.Future):
            loop.stop()

        future = asyncio.ensure_future(runner(), loop=loop)
        future.add_done_callback(stop_loop_on_completion)

        try:
            loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            future.remove_done_callback(stop_loop_on_completion)
            self.utils.cleanup_loop(loop)

    async def _voice_server_update(self, data: discord_typings.VoiceServerUpdateData):
        payload = {
            "token": data["token"],
            "endpoint": data["endpoint"],
            "guild_id": data["guild_id"],
        }

        if data["endpoint"]:
            payload["endpoint"] = data["endpoint"]

        await self.dispatch("voice_server_update", payload)

    async def _voice_state_update(self, data: discord_typings.VoiceStateUpdateData):
        from EpikCord import VoiceState

        await self.dispatch(
            "voice_state_update", VoiceState(self, data)
        )  # TODO: Make this return something like (VoiceState, Member) or make VoiceState get Member from member_id

    async def _guild_delete(self, data: discord_typings.GuildDeleteData):
        if guild := self.guilds.remove_from_cache(data["id"]):
            await self.dispatch("guild_delete", guild)

    async def _interaction_create(self, data: discord_typings.InteractionCreateData):
        interaction = self.utils.interaction_from_type(data)
        await self.dispatch("interaction_create", interaction)

    async def _channel_create(self, data: discord_typings.ChannelCreateData):
        channel = self.utils.channel_from_type(data)
        self.channels.add_to_cache(channel.id, channel)
        await self.dispatch("channel_create", channel)

    async def _message_create(self, data: discord_typings.MessageCreateData):
        """Event fired when messages are created"""
        from EpikCord import Message

        await self.dispatch("message_create", Message(self, data))

    async def _guild_create(self, data: discord_typings.GuildCreateData):
        from EpikCord import Guild, Thread, UnavailableGuild

        if data.get("unavailable") is None:
            return  # TODO: Maybe a different event where the name says the Bot is removed on startup.

        guild: Union[UnavailableGuild, Guild] = (
            UnavailableGuild(data) if data.get("unavailable") else Guild(self, data)
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

        await self.dispatch("guild_create", guild)
        # TODO: Add other attributes to cache

    async def _guild_member_update(self, data: discord_typings.GuildMemberUpdateData):
        from EpikCord import GuildMember

        guild_member = GuildMember(self, data)  # type: ignore
        guild = self.guilds.get(data["guild_id"])
        if not guild:
            guild = await self.guilds.fetch(int(data["guild_id"]))
        if not guild:
            logger.critical("Guild was not found in cache, and could not be fetched.")

        guild.members.cache[guild_member.id] = guild_member
        await self.dispatch("guild_member_update", guild_member)

    async def _ready(self, data: discord_typings.ReadyData):
        from EpikCord import ClientApplication, ClientUser

        self.user = ClientUser(self, data["user"])
        self.session_id = data["session_id"]
        self.resume_gateway_url = data["resume_gateway_url"]
        application_response = await self.http.get("/oauth2/applications/@me")
        application_data = await application_response.json()

        self.application = ClientApplication(self, application_data)

        await self.dispatch("ready")


__all__ = ("WebsocketClient", "Event")
