"""
NOTE: version string only in setup.cfg
"""
from __future__ import annotations

import asyncio
import struct
import zlib
from .rtp_handler import *
import datetime
import io
import os
import re
import socket
from base64 import b64encode
from collections import defaultdict, deque
from importlib import import_module
from inspect import iscoroutine
from logging import getLogger
from time import perf_counter_ns
from .type_enums import *
from sys import platform
from typing import (
    Optional,
    List,
    Union,
    Dict,
    TypeVar,
    Callable,
    Tuple,
    Any,
    Type,
    TYPE_CHECKING,
)
from urllib.parse import quote as _quote

from aiohttp import ClientSession, ClientResponse, ClientWebSocketResponse

from .__main__ import __version__
from .close_event_codes import *
from .status_code import *
from .components import *
from .exceptions import *
from .managers import *
from .opcodes import *
from .options import *
from .partials import *

CT = TypeVar("CT", bound="Colour")
T = TypeVar("T")
logger = getLogger(__name__)

try:
    import nacl
except ImportError:
    logger.warning(
        "The PyNacl library was not found, so voice is not supported."
        " Please install it by doing ``pip install PyNaCl``"
        " If you want voice support"
    )

_ORJSON = False

try:
    import orjson as json

    _ORJSON = True

except ImportError:
    import json

"""
:license:
Some parts of the code is sourced from discord.py
The MIT License (MIT)
Copyright © 2015-2021 Rapptz
Copyright © 2021-present EpikHost
Permission is hereby granted, free of charge, to any person obtaining a copy of 
this software and associated documentation files (the “Software”), to deal in 
the Software without restriction, including without limitation the rights to 
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies 
of the Software, and to permit persons to whom the Software is furnished to do 
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all 
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, RESS OR IMPLIED,
 INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A 
 PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR 
 COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER 
 IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN 
 CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE."""


class Localization:
    def __init__(self, locale: Locale, value: str):
        self.locale: Locale = str(locale)
        self.value: str = value

    def to_dict(self):
        return {self.locale: self.value}


Localisation = Localization


class Status:
    """The class which represents a Status.

    Attributes
    ----------
    status : str
        The status of the user.
    """

    def __init__(self, status: str):
        """Represents a Status.

        Arguments
        ---------
        status : str
            The status of the user.
            Either ``online``, ``idle``, ``dnd`` or ``invisible``.

        Raises
        ------
        InvalidStatus
            The status that you supplied is not valid.
        """
        if status in {"online", "dnd", "idle", "invisible", "offline"}:
            setattr(self, "status", status if status != "offline" else "invisible")
        else:
            raise InvalidStatus("That is an invalid status.")


class Activity:
    """Represents a Discord Activity object.

    Attributes
    ---------
    name : str
        The name of the activity.
    type : int
        The type of the activity.
    url : Optional[str]
        The url of the activity.
        Only available for the streaming activity

    """

    def __init__(self, *, name: str, type: int, url: Optional[str] = None):
        """Represents a Discord Activity object.

        Arguments
        ---------
        name : str
            The name of the activity.
        type : int
            The type of the activity.
        url : Optional[str]
            The url of the activity.
            Only available for the streaming activity.
        """
        self.name = name
        self.type = type
        self.url = url

    def to_dict(self):
        """Returns activity class as dict

        Returns
        -------
        payload : dict
            The dict representation of the Activity.

        Raises
        ------
            InvalidData
                You tried to set an url for a non-streaming activity.
        """
        payload = {
            "name": self.name,
            "type": self.type,
        }

        if self.url:
            if self.type != 1:
                raise InvalidData("You cannot set a URL")
            payload["url"] = self.url

        return payload


class Presence:
    """
    A class representation of a Presence.

    Attributes
    ----------
    activity : Optional[Activity]
        The activity of the user.
    status : Status
        The status of the user.
    """

    def __init__(
        self,
        *,
        activity: Optional[List[Activity]] = None,
        status: Optional[Status] = None,
    ):
        """
        Arguments
        ---------
        activity : Optional[Activity]
            The activity of the user.
        status : Status
            The status of the user.
        """
        self.activity: Optional[List[Activity]] = activity
        self.status: Status = status.status if isinstance(status, Status) else status

    def to_dict(self):
        """
        The dict representation of the Presence.

        Returns
        -------
        payload : dict
            The dict representation of the Presence.
        """
        payload = {}

        if self.status:
            payload["status"] = self.status

        if self.activity:
            payload["activity"] = [self.activity.to_dict()]

        return payload


class UnavailableGuild:
    """
    The class representation of an UnavailableGuild.
    The Guild object should be given to use when the guild is available.
    """

    def __init__(self, data):
        self.data = data
        self.id: str = data.get("id")
        self.available: bool = data.get("available")


class Reaction:
    """
    A class representation of a Reaction.
    Not for direct use.


    Attributes
    ----------
    count : int
        The amount of times this reaction has been added to the Message.
    me : bool
        If the ClientUser has reacted to this Message with this Reaction.
    emoji : PartialEmoji
        The partial emoji of this Reaction.
    """

    def __init__(self, data: dict):
        self.count: int = data.get("count")
        self.me: bool = data.get("me")
        self.emoji: PartialEmoji = PartialEmoji(data.get("emoji"))


class Message:
    """Represents a Discord message.

    Attributes
    ----------
    client : Client
        The client which initialised this Message.
    id : str
        The message ID.
    channel_id : str
        The channel ID the message was sent in.
    author : Union[GuildMember, User]
        The author of the message
    guild_id: str
        The Guild ID the message was sent in

    """

    def __init__(self, client, data: dict):
        self.client = client
        self.id: str = data.get("id")
        self.channel_id: str = data.get("channel_id")
        self.channel = client.channels.get(self.channel_id)
        self.guild_id: Optional[str] = data.get("guild_id")
        self.webhook_id: Optional[str] = data.get("webhook_id")
        self.author: Optional[Union[WebhookUser, GuildMember, User]] = None
        if self.webhook_id:
            self.author = WebhookUser(data.get("author"))
        if data.get("member"):
            member_data = data["member"]
            if data.get("author"):
                member_data["user"] = data["author"]
            self.author = GuildMember(self, member_data)
        else:
            self.author = User(self, data.get("author")) if data.get("author") else None

        # member_data = data.get("member") if data.get("member") else data.get("000")
        # self.author: Optional[Union[WebhookUser, User]] = (
        #     WebhookUser(data.get("author"))
        #     if data.get("webhook_id")
        #     else GuildMember(client, member_data)
        #     if data.get("member")
        #     else User(client, data.get("author"))
        #     if data.get("author")
        #     else None
        # )
        # I forgot Message Intents are gonna stop this.
        self.content: Optional[str] = data.get("content")
        self.timestamp: datetime.datetime = datetime.datetime.fromisoformat(
            data["timestamp"]
        )
        self.edited_timestamp: Optional[str] = (
            datetime.datetime.fromisoformat(data.get("edited_timestamp"))
            if data.get("edited_timestamp")
            else None
        )
        self.tts: bool = data.get("tts")
        self.mention_everyone: bool = data.get("mention_everyone")
        self.mentions: Optional[List[User]] = [
            User(client, user) for user in data.get("mentions", [])
        ]
        self.mention_roles: Optional[List[int]] = data.get("mention_roles")
        self.mention_channels: Optional[List[MentionedChannel]] = [
            MentionedChannel(channel) for channel in data.get("mention_channels", [])
        ]
        self.embeds: Optional[List[Embed]] = [
            Embed(**embed) for embed in data.get("embeds", [])
        ]
        self.reactions: Optional[List[Reaction]] = [
            Reaction(reaction) for reaction in data.get("reactions", [])
        ]
        self.nonce: Optional[Union[int, str]] = data.get("nonce")
        self.pinned: bool = data.get("pinned")
        self.type: int = data.get("type")
        self.activity: Optional[MessageActivity] = (
            MessageActivity(data.get("activity")) if data.get("activity") else None
        )
        # Despite there being a PartialApplication,
        # Discord don't specify what attributes it has
        self.application: Application = (
            Application(data.get("application")) if data.get("application") else None
        )
        self.flags: int = data.get("flags")
        self.referenced_message: Optional[Message] = (
            Message(client, data.get("referenced_message"))
            if data.get("referenced_message")
            else None
        )
        self.interaction: Optional[MessageInteraction] = (
            MessageInteraction(client, data.get("interaction"))
            if data.get("interaction")
            else None
        )
        self.thread: Optional[Thread] = (
            Thread(data.get("thread")) if data.get("thread") else None
        )
        self.components: Optional[List[Union[TextInput, SelectMenu, Button]]] = [
            ActionRow.from_dict(component) for component in data.get("components")
        ]
        self.stickers: Optional[List[StickerItem]] = [
            StickerItem(sticker) for sticker in data.get("stickers", [])
        ] or None

    async def add_reaction(self, emoji: str):
        emoji = _quote(emoji)
        response = await self.client.http.put(
            f"channels/{self.channel_id}/messages/{self.id}/reactions/{emoji}/@me"
        )
        return await response.json()

    async def remove_reaction(self, emoji: str, user=None):
        emoji = _quote(emoji)
        response = (
            await self.client.http.delete(
                f"channels/{self.channel_id}/messages/{self.id}/reactions/{emoji}/{user.id}"
            )
            if user
            else await self.client.http.delete(
                f"channels/{self.channel_id}/messages/{self.id}/reactions/{emoji}/@me"
            )
        )

        return await response.json()

    async def fetch_reactions(self, *, after, limit) -> List[Reaction]:
        response = await self.client.http.get(
            f"channels/{self.channel_id}/messages/{self.id}/reactions?after={after}&limit={limit}"
        )
        return await response.json()

    async def delete_all_reactions(self):
        response = await self.client.http.delete(
            f"channels/{self.channel_id}/messages/{self.id}/reactions"
        )
        return await response.json()

    async def delete_reaction_for_emoji(self, emoji: str):
        emoji = _quote(emoji)
        response = await self.client.http.delete(
            f"channels/{self.channel_id}/messages/{self.id}/reactions/{emoji}"
        )
        return await response.json()

    async def edit(self, message_data: dict):
        response = await self.client.http.patch(
            f"channels/{self.channel_id}/messages/{self.id}", data=message_data
        )
        return await response.json()

    async def delete(self):
        response = await self.client.http.delete(
            f"channels/{self.channel_id}/messages/{self.id}"
        )
        return await response.json()

    async def pin(self, *, reason: Optional[str]):
        headers = self.client.http.headers.copy()
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        else:
            logger.debug(f"Pinning message {self.id}.")
        response = await self.client.http.put(
            f"channels/{self.channel_id}/pins/{self.id}", headers=headers
        )
        return await response.json()

    async def unpin(self, *, reason: Optional[str]):
        headers = self.client.http.headers.copy()
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        response = await self.client.http.delete(
            f"channels/{self.channel_id}/pins/{self.id}", headers=headers
        )
        return await response.json()

    async def start_thread(
        self,
        name: str,
        auto_archive_duration: Optional[int],
        rate_limit_per_user: Optional[int],
    ):
        response = await self.client.http.post(
            f"channels/{self.channel_id}/messages/{self.id}/threads",
            data={
                "name": name,
                "auto_archive_duration": auto_archive_duration,
                "rate_limit_per_user": rate_limit_per_user,
            },
        )
        # Cache it
        self.client.guilds[self.guild_id].append(Thread(await response.json()))
        return Thread(await response.json())

    async def crosspost(self):
        response = await self.client.http.post(
            f"channels/{self.channel_id}/messages/{self.id}/crosspost"
        )
        return await response.json()


class File:
    """
    Represents a file. Sourced from Discord.py
    """

    def __init__(
        self,
        fp: Union[str, bytes, os.PathLike, io.BufferedIOBase],
        filename: Optional[str] = None,
        *,
        spoiler: bool = False,
    ):
        if isinstance(fp, io.IOBase):
            if not (fp.seekable() and fp.readable()):
                raise ValueError(f"File buffer {fp!r} must be seekable and readable")
            self.fp = fp
            self._original_pos = fp.tell()
        else:
            self.fp = open(fp, "rb")
            self._original_pos = 0
        self._closer = self.fp.close
        self.fp.close = lambda: None

        if filename is None:
            if isinstance(fp, str):
                _, self.filename = os.path.split(fp)
            else:
                self.filename = getattr(fp, "name", None)
        else:
            self.filename = filename
        if (
            spoiler
            and self.filename is not None
            and not self.filename.startswith("SPOILER_")
        ):
            self.filename = f"SPOILER_{self.filename}"

            self.spoiler = spoiler or (
                self.filename is not None and self.filename.startswith("SPOILER_")
            )

    def reset(self, *, seek: Union[int, bool] = True) -> None:
        if seek:
            self.fp.seek(self._original_pos)

    def close(self) -> None:
        self.fp.close = self._closer
        self._closer()


class Messageable:
    def __init__(self, client, channel_id: str):
        self.id: str = channel_id
        self.client = client

    async def fetch_messages(
        self,
        *,
        around: Optional[str] = None,
        before: Optional[str] = None,
        after: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> List[Message]:
        response = await self.client.http.get(
            f"channels/{self.id}/messages",
            params={"around": around, "before": before, "after": after, "limit": limit},
        )
        data = await response.json()
        return [Message(self.client, message) for message in data]

    async def fetch_message(self, *, message_id: str) -> Message:
        response = await self.client.http.get(
            f"channels/{self.id}/messages/{message_id}"
        )
        data = await response.json()
        return Message(self.client, data)

    async def send(
        self,
        content: Optional[str] = None,
        *,
        embeds: Optional[List[dict]] = None,
        components=None,
        tts: Optional[bool] = False,
        allowed_mentions=None,
        sticker_ids: Optional[List[str]] = None,
        attachments: List[File] = None,
        suppress_embeds: bool = False,
    ) -> Message:
        payload = {}

        if content:
            payload["content"] = content

        if embeds:
            payload["embeds"] = [embed.to_dict() for embed in embeds]

        if components:
            payload["components"] = [component.to_dict() for component in components]

        if tts:
            payload["tts"] = tts

        if allowed_mentions:
            payload["allowed_mentions"] = allowed_mentions.to_dict()

        if sticker_ids:
            payload["sticker_ids"] = sticker_ids

        if attachments:
            payload["attachments"] = [
                attachment.to_dict() for attachment in attachments
            ]

        if suppress_embeds:
            payload["suppress_embeds"] = 1 << 2

        response = await self.client.http.post(
            f"channels/{self.id}/messages", json=payload
        )
        data = await response.json()
        return Message(self.client, data)


class User(Messageable):
    def __init__(self, client, data: dict):
        super().__init__(client, data["id"])
        self.data = data
        self.client = client
        self.id: str = data.get("id")
        self.username: str = data.get("username")
        self.discriminator: str = data.get("discriminator")
        self.avatar: Optional[str] = data.get("avatar")
        self.bot: Optional[bool] = data.get("bot")
        self.system: Optional[bool] = data.get("system")
        self.mfa_enabled: bool = data.get("mfa_enabled")
        self.banner: Optional[str] = data.get("banner")
        # the user's banner color encoded as an integer representation of
        # hexadecimal color code
        self.accent_color: Optional[int] = data.get("accent_color")
        self.locale: Optional[str] = data.get("locale")
        self.verified: bool = data.get("verified")
        self.email: Optional[str] = data.get("email")
        self.flags: int = data.get("flags")
        self.premium_type: int = data.get("premium_type")
        self.public_flags: int = data.get("public_flags")


class VoiceRegion:
    def __init__(self, data: dict):
        self.id: str = data["id"]
        self.name: str = data["name"]
        self.optimal: bool = data["optimal"]
        self.deprecated: bool = data["deprecated"]
        self.custom: bool = data["custom"]


class EventHandler:
    # Class that'll contain all methods that'll be called when an event is
    # triggered.

    def __init__(self):
        self.events = defaultdict(list)
        self.wait_for_events = defaultdict(list)
        self.latencies = deque(maxlen=5)

    def wait_for(
        self, event_name: str, *, check: Optional[Callable] = None, timeout: int = None
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
        timeout = timeout or 0
        future = asyncio.Future()
        if not check:

            def check(*_, **__):
                return True

        self.wait_for_events[event_name.lower()].append((future, check))
        return asyncio.wait_for(future, timeout=timeout)

    @staticmethod
    async def voice_server_update(data: dict):
        voice_data = data["d"]
        payload = {
            "token": voice_data["token"],
            "endpoint": voice_data["endpoint"],
            "guild_id": voice_data["guild_id"],
        }

        if voice_data["endpoint"]:
            payload["endpoint"] = voice_data["endpoint"]

        return payload

    async def voice_state_update(self, data: dict):
        return VoiceState(
            self, data
        )  # TODO: Make this return something like (VoiceState, Member) or make VoiceState get Member from member_id

    def component(self, custom_id: str):
        """
        Execute this function when a component with the `custom_id` is interacted with.
        """

        def wrapper(func):
            self._components[custom_id] = func

        return wrapper

    async def guild_members_chunk(self, data: dict):
        ...

    async def guild_delete(self, data: dict):
        return self.guilds.get(data["id"])

    async def handle_events(self):
        async for event in self.ws:
            event = event.json()
            logger.debug(f"Received {event} from Discord.")

            if event["op"] == GatewayOpcode.HELLO:
                self.interval = event["d"]["heartbeat_interval"]

                async def wrapper():
                    while True:
                        await self.heartbeat(False)

                asyncio.create_task(wrapper())
                await self.identify()

            elif event["op"] == GatewayOpcode.DISPATCH:
                await self.handle_event(event)
            elif event["op"] == GatewayOpcode.HEARTBEAT:
                # I shouldn't wait the remaining delay according to the docs.
                await self.heartbeat(True)

            elif event["op"] == GatewayOpcode.HEARTBEAT_ACK:
                heartbeat_ack_time = perf_counter_ns()
                self.discord_latency: int = heartbeat_ack_time - self.heartbeat_time
                self.latencies.append(self.discord_latency)
                try:
                    self.heartbeats.append(event["d"])
                except AttributeError:
                    self.heartbeats = [event["d"]]

            elif event["op"] == GatewayOpcode.RECONNECT:
                await self.reconnect()

            elif event["op"] == GatewayOpcode.RESUMED:
                logger.debug(
                    "Connection successfully resumed and all proceeding events are new."
                )

            if event["op"] != GatewayOpcode.DISPATCH:  # TODO: find op code
                logger.debug(f"Received OPCODE: {event['op']}")

        await self.handle_close()

    async def handle_event(self, event: dict):
        self.sequence = event["s"]
        logger.info(f"Received event {event['t']} with data {event['d']}")

        results_from_event = event["d"]

        try:
            results_from_event = (
                await getattr(self, event["t"].lower())(results_from_event)
                if hasattr(self, event["t"].lower())
                else None
            )
            if not results_from_event:
                results_from_event = []
        except Exception as e:
            logger.exception(f"Error handling event {event['t']}: {e}")

        if isinstance(results_from_event, UnavailableGuild):
            return  # This is their lazy backfil which I dislike.

        try:
            if results_from_event != event["d"]:
                results_from_event = [results_from_event] if results_from_event else []
                if callbacks := self.events.get(event["t"].lower()):
                    logger.info(
                        f"Calling {len(callbacks)} callbacks for {event['t']} with data {results_from_event}"
                    )
                    for callback in callbacks:
                        await callback(*results_from_event)
            else:
                logger.warning(f"{event['t']} is going to receive unparsed data.")

                if callbacks := self.events.get(event["t"].lower()):
                    for callback in callbacks:
                        await callback(results_from_event)
        except Exception as e:
            logger.exception(f"Error handling user-defined event {event['t']}: {e}")
        if callbacks := self.wait_for_events.get(event["t"].lower()):
            for future, check in callbacks:
                if check(*results_from_event):
                    future.set_result(results_from_event)

    async def handle_interaction(self, interaction):
        """The function which is the handler for interactions.
        Change this if you want to, to change how your "command handler" works

        Arguments
        ---------
        interaction: Union[ApplicationCommandInteraction, MessageComponentInteraction, AutoCompleteInteraction, ModalSubmitInteraction]
            A subclass of BaseInteraction which represents the Interaction
        """

        if interaction.is_ping:
            return await self.http.post(
                f"interactions/{interaction.id}/{interaction.token}/callback",
                json={"type": 1},
            )

        elif interaction.is_application_command:
            command = self.commands.get(interaction.command_name)

            if not command:
                logger.warning(
                    f"Command {interaction.command_name} is not registered in "
                    f"this code, but is registered with Discord. "
                )
                return  # TODO Possibly add an error which people can handle?

            options = []

            if command.is_user_command() or command.is_message_command():
                options.append(interaction.target_id)

            if command.is_slash_command():
                for check in command.checks:
                    if iscoroutine(check):
                        await check.callback(interaction)
                    else:
                        check.callback(interaction)

                for option in interaction.options:
                    options.append(option.get("value"))

            return await command.callback(interaction, *options)

        if interaction.is_message_component:  # If it's a message component interaction

            if not self._components.get(
                interaction.custom_id
            ):  # If it's registered with the bot
                logger.warning(
                    f"A user tried to interact with a component with the "
                    f"custom id {interaction.custom_id}, but it is not "
                    f"registered in this code, but is on Discord. "
                )

            if interaction.is_button():  # If it's a button
                return await self._components[interaction.custom_id](
                    interaction, self.utils.interaction_from_type(component)
                )  # Call the callback

            elif interaction.is_select_menu():

                def get_select_menu():
                    for action_row in interaction.message.components:
                        for component in action_row["components"]:
                            if component["custom_id"] == interaction.custom_id:
                                component = self.utils.component_from_type(component)
                                return component

                return await self._components[interaction.custom_id](
                    interaction, get_select_menu(), *interaction.values
                )

        if interaction.is_autocomplete:
            command = self.commands.get(interaction.command_name)
            if not command:
                return
            ...  # TODO: Implement autocomplete

        if interaction.is_modal_submit:
            action_rows = interaction._components
            component_object_list = []
            for action_row in action_rows:
                for component in action_row.get("components"):
                    component_object_list.append(
                        component["value"]
                    )  # TODO: Fix this later, component_object_list is empty ;(

            await self._components.get(interaction.custom_id)(
                interaction, *component_object_list
            )

    async def interaction_create(self, data):
        interaction = self.utils.interaction_from_type(data)

        await self.handle_interaction(interaction)

        return interaction

    async def channel_create(self, data: dict):
        channel = self.utils.channel_from_type(data)
        self.channels.add_to_cache(channel.id, channel)
        return channel

    async def message_create(self, data: dict):
        """Event fired when messages are created"""
        return Message(self, data)

    async def guild_create(self, data):
        guild = (
            UnavailableGuild(data)
            if data.get("unavailable") is True
            else Guild(self, data)
            if data.get("unavailable") is False
            else None
        )

        if not guild:
            return

        self.guilds.add_to_cache(guild.id, guild)

        if data.get("unavailable") is None:
            return  # Bot was removed

        for channel in data["channels"]:
            self.channels.add_to_cache(
                data["id"], self.utils.channel_from_type(channel)
            )

        for thread in data["threads"]:
            self.channels.add_to_cache(data["id"], self.utils.channel_from_type(thread))

        return guild

        # TODO: Add other attributes to cache

    def event(self, event_name: Optional[str] = None):
        def register_event(func):
            func_name = event_name or func.__name__.lower()

            if func_name.startswith("on_"):
                func_name = func_name[3:]

            self.events[func_name].append(func)

            return Event(func, event_name=func_name)

        return register_event

    async def guild_member_update(self, data):
        guild_member = GuildMember(self, data)
        return self.members.fetch(data["id"]), guild_member

    async def ready(self, data: dict):
        self.user: ClientUser = ClientUser(self, data.get("user"))
        self.session_id: str = data["session_id"]
        application_response = await self.http.get("/oauth2/applications/@me")
        application_data = await application_response.json()
        self.application: ClientApplication = ClientApplication(self, application_data)

        if self.overwrite_commands_on_ready:

            command_sorter = defaultdict(list)

            for command in self.commands.values():
                command_payload = {"name": command.name, "type": command.type}

                if command_payload["type"] == 1:
                    command_payload["description"] = command.description
                    command_payload["options"] = [
                        option.to_dict() for option in getattr(command, "options", [])
                    ]
                    if command.name_localizations:
                        command_payload["name_localizations"] = {}
                        for name_localization in command.name_localizations:
                            command_payload["name_localizations"][
                                name_localization
                            ] = command.name_localizations[name_localization.to_dict()]
                    if command.description_localizations:
                        command_payload["description_localizations"] = {}
                        for (
                            description_localization
                        ) in command.description_localizations:
                            command_payload["description_localizations"][
                                description_localization.to_dict()
                            ] = command.description_localizations[
                                description_localization
                            ]

                for guild_id in command.guild_ids or []:
                    command_sorter[guild_id].append(command_payload)
                else:
                    command_sorter["global"].append(command_payload)

            for guild_id, commands in command_sorter.items():

                if guild_id == "global":
                    await self.application.bulk_overwrite_global_application_commands(
                        commands
                    )
                    continue

                await self.application.bulk_overwrite_guild_application_commands(
                    guild_id, commands
                )
        return None


class WebsocketClient(EventHandler):
    def __init__(self, token: str, intents: int):
        super().__init__()

        self.token = token
        if not token:
            raise TypeError("Missing token.")

        if isinstance(intents, int):
            self.intents = Intents(intents)
        elif isinstance(intents, Intents):
            self.intents = intents

        self.commands = {}
        self._closed = True
        self.heartbeats = []

        self.interval = None  # How frequently to heartbeat
        self.session_id = None
        self.sequence = None

    async def change_presence(self, *, presence: Optional[Presence]):
        payload = {"op": GatewayOpcode.PRESENCE_UPDATE, "d": presence.to_dict()}
        await self.send_json(payload)

    async def heartbeat(self, forced: Optional[bool] = None):
        if forced:
            return await self.send_json(
                {"op": GatewayOpcode.HEARTBEAT, "d": self.sequence or "null"}
            )

        if self.interval:
            await self.send_json(
                {"op": GatewayOpcode.HEARTBEAT, "d": self.sequence or "null"}
            )
            self.heartbeat_time = perf_counter_ns()
            await asyncio.sleep(self.interval / 1000)
            logger.debug("Sent a heartbeat!")

    async def request_guild_members(
        self,
        guild_id: int,
        *,
        query: Optional[str] = None,
        limit: Optional[int] = None,
        presences: Optional[bool] = None,
        user_ids: Optional[List[str]] = None,
        nonce: Optional[str] = None,
    ):
        payload = {
            "op": GatewayOpcode.REQUEST_GUILD_MEMBERS,
            "d": {"guild_id": guild_id},
        }

        if query:
            payload["d"]["query"] = query

        if limit:
            payload["d"]["limit"] = limit

        if presences:
            payload["d"]["presences"] = presences

        if user_ids:
            payload["d"]["user_ids"] = user_ids

        if nonce:
            payload["d"]["nonce"] = nonce

        await self.send_json(payload)

    async def reconnect(self):
        await self.close()
        await self.connect()
        await self.identify()
        await self.resume()

    async def handle_close(self):
        if self.ws.close_code == GatewayCECode.DisallowedIntents:
            raise DisallowedIntents(
                "You cannot use privileged intents with this token, go to "
                "the developer portal and allow the privileged intents "
                "needed. "
            )
        elif self.ws.close_code == 1006:
            await self.resume()
        elif self.ws.close_code == GatewayCECode.AuthenticationFailed:
            raise InvalidToken("The token you provided is invalid.")
        elif self.ws.close_code == GatewayCECode.RateLimited:
            raise Ratelimited429(
                "You've been rate limited. Try again in a few minutes."
            )
        elif self.ws.close_code == GatewayCECode.ShardingRequired:
            raise ShardingRequired("You need to shard the bot.")
        elif self.ws.close_code == GatewayCECode.InvalidAPIVersion:
            raise DeprecationWarning(
                "The gateway you're connecting to is deprecated and does not "
                "work, upgrade EpikCord.py. "
            )
        elif self.ws.close_code == GatewayCECode.InvalidIntents:
            raise InvalidIntents("The intents you provided are invalid.")
        elif self.ws.close_code == GatewayCECode.UnknownError:
            await self.resume()
        elif self.ws.close_code == GatewayCECode.UnknownOpcode:
            logger.critical(
                "EpikCord.py sent an invalid OPCODE to the Gateway. "
                "Report this immediately. "
            )
            await self.resume()
        elif self.ws.close_code == GatewayCECode.DecodeError:
            logger.critical(
                "EpikCord.py sent an invalid payload to the Gateway."
                " Report this immediately. "
            )
            await self.resume()
        elif self.ws.close_code == GatewayCECode.NotAuthenticated:
            logger.critical(
                "EpikCord.py has sent a payload prior to identifying."
                " Report this immediately. "
            )

        elif self.ws.close_code == GatewayCECode.AlreadyAuthenticated:
            logger.critical(
                "EpikCord.py tried to authenticate again." " Report this immediately. "
            )
            await self.resume()
        elif self.ws.close_code == GatewayCECode.InvalidSequence:
            logger.critical(
                "EpikCord.py sent an invalid sequence number."
                " Report this immediately."
            )
            await self.resume()
        elif self.ws.close_code == GatewayCECode.SessionTimeout:
            logger.critical("Session timed out.")
            await self.resume()
        else:
            raise ClosedWebSocketConnection(
                f"Connection has been closed with code {self.ws.close_code}"
            )

    async def send_json(self, json: dict):
        await self.ws.send_json(json)
        logger.debug(f"Sent {json} to the Websocket Connection to Discord.")

    async def connect(self):
        res = await self.http.get("/gateway")
        data = await res.json()
        url = data["url"]
        self.ws = await self.http.ws_connect(
            f"{url}?v=10&encoding=json&compress=zlib-stream"
        )
        self._closed = False
        await self.handle_events()

    async def resume(self):
        logger.critical("Reconnecting...")
        await self.connect()
        await self.send_json(
            {
                "op": GatewayOpcode.RESUME,
                "d": {
                    "seq": self.sequence,
                    "session_id": self.session_id,
                    "token": self.token,
                },
            }
        )
        self._closed = False

    async def identify(self):
        payload = {
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
        if self.presence:
            payload["d"]["presence"] = self.presence.to_dict()
        return await self.send_json(payload)

    async def close(self) -> None:
        if self._closed:
            return

        # for voice in self.voice_clients:
        #     try:
        #         await voice.disconnect(force=True)
        #     except Exception:
        #         # if an error happens during disconnects, disregard it.
        #         pass

        if self.ws is not None and not self.ws.closed:
            await self.ws.close(code=4000)

        if self.http is not None and not self.http.closed:
            await self.http.close()

        self._closed = True

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


class BaseCommand:
    def __init__(self):
        self.checks: List[Check] = []

    def is_slash_command(self):
        return self.type == 1

    def is_user_command(self):
        return self.type == 2

    def is_message_command(self):
        return self.type == 3


class ClientUserCommand(BaseCommand):
    """
    A class to represent a User Command that the Client owns.

    Attributes:
    -----------
        * name The name set for the User Command
        * callback: callable The function to call for the User Command
        (Passed in by the library)

    Parameters:
    -----------
    All parameters follow the documentation of the Attributes accordingly
        * name
        * callback
    """

    def __init__(self, *, name: str, callback: Callable):
        super().__init__()
        self.name: str = name
        self.callback: Callable = callback

    @property
    def type(self):
        return 2


class ClientSlashCommand(BaseCommand):
    def __init__(
        self,
        *,
        name: str,
        description: str,
        callback: Callable,
        guild_ids: Optional[List[str]],
        options: Optional[List[AnyOption]],
        name_localization: Optional[Localization] = None,
        description_localization: Optional[str] = None,
    ):
        super().__init__()
        self.name: str = name
        self.description: str = description
        self.name_localizations: Optional[Localization] = name_localization
        self.description_localizations: Optional[
            Localization
        ] = description_localization
        if not description:
            raise TypeError(f"Missing description for command {name}.")
        self.callback: Callable = callback
        self.guild_ids: Optional[List[str]] = guild_ids
        self.options: Optional[List[AnyOption]] = options
        self.autocomplete_options: dict = {}

    @property
    def type(self):
        return 1

    def option_autocomplete(self, option_name: str):
        def wrapper(func):
            self.autocomplete_options[option_name] = func

        return wrapper

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "type": self.type,
            "options": [option.to_dict() for option in options],
            "name_localization": self.name_localization,
            "description_localization": self.description_localization,
        }


class ClientMessageCommand(ClientUserCommand):
    @property
    def type(self):
        return 3


class Overwrite:
    def __init__(self, data: dict):
        self.id: str = data.get("id")
        self.type: int = data.get("type")
        self.allow: str = data.get("allow")
        self.deny: str = data.get("deny")


class StickerItem:
    def __init__(self, data: dict):
        self.id: str = data.get("id")
        self.name: str = data.get("name")
        self.format_type: int = data.get("format_type")


class Sticker:
    def __init__(self, data: dict):
        self.id: str = data.get("id")
        self.name: str = data.get("name")
        self.description: str = data.get("description")
        self.tags: str = data.get("tags")
        self.type: str = data.get("image")
        self.format_type: int = data.get("format_type")
        self.pack_id: int = data.get("pack_id")
        self.sort_value: int = data.get("sort_value")


class ThreadMember:
    def __init__(self, data: dict):
        self.id: str = data.get("user_id")
        self.thread_id: str = data.get("thread_id")
        self.join_timestamp: datetime.datetime = datetime.datetime.fromisoformat(
            data["join_timestamp"]
        )
        self.flags: int = data.get("flags")


class Thread:
    def __init__(self, client, data: dict):
        super().__init__(client, data)
        self.owner_id: str = data.get("owner_id")
        self.message_count: int = data.get("message_count")
        self.member_count: int = data.get("member_count")
        self.archived: bool = data.get("archived")
        self.auto_archive_duration: int = data.get("auto_archive_duration")
        self.archive_timestamp: datetime.datetime = datetime.datetime.fromisoformat(
            data["archive_timestamp"]
        )
        self.locked: bool = data.get("locked")

    async def join(self):
        if self.archived:
            raise ThreadArchived(
                "This thread has been archived so it is no longer joinable"
            )
        response = await self.client.http.put(
            f"/channels/{self.id}/thread-members/@me", channel_id=self.id
        )
        return await response.json()

    async def add_member(self, member_id: str):
        if self.archived:
            raise ThreadArchived(
                "This thread has been archived so it is no longer joinable"
            )

        response = await self.client.http.put(
            f"/channels/{self.id}/thread-members/{member_id}", channel_id=self.id
        )
        return await response.json()

    async def leave(self):
        if self.archived:
            raise ThreadArchived(
                "This thread has been archived so it is no longer leaveable"
            )
        response = await self.client.http.delete(
            f"/channels/{self.id}/thread-members/@me", channel_id=self.id
        )
        return await response.json()

    async def remove_member(self, member_id: str):
        if self.archived:
            raise ThreadArchived(
                "This thread has been archived so it is no longer leaveable"
            )

        response = await self.client.http.delete(
            f"/channels/{self.id}/thread-members/{member_id}", channel_id=self.id
        )
        return await response.json()

    async def fetch_member(self, member_id: str) -> ThreadMember:
        response = await self.client.http.get(
            f"/channels/{self.id}/thread-members/{member_id}", channel_id=self.id
        )
        if response.status == 404:
            raise NotFound404("The member you are trying to fetch does not exist")
        return ThreadMember(await response.json())

    async def list_members(self) -> List[ThreadMember]:
        response = await self.client.http.get(
            f"/channels/{self.id}/thread-members", channel_id=self.id
        )
        return [ThreadMember(member) for member in await response.json()]

    async def bulk_delete(self, message_ids: List[str], reason: Optional[str]) -> None:

        if reason:
            headers = self.client.http.headers.copy()
            headers["X-Audit-Log-Reason"] = reason

        response = await self.client.http.post(
            f"channels/{self.id}/messages/bulk-delete",
            data={"messages": message_ids},
            headers=headers,
            channel_id=self.id,
        )
        return await response.json()


class PrivateThread(Thread):
    ...


class Application:
    def __init__(self, data: dict):
        self.id: str = data.get("id")
        self.name: str = data.get("name")
        self.icon: Optional[str] = data.get("icon")
        self.description: str = data.get("description")
        self.rpc_origins: Optional[list] = data.get("rpc_origins")
        self.bot_public: bool = data.get("bot_public")
        self.bot_require_code_grant: bool = data.get("bot_require_code_grant")
        self.terms_of_service_url: Optional[str] = data.get("terms_of_service")
        self.privacy_policy_url: Optional[str] = data.get("privacy_policy")
        self.owner: Optional[PartialUser] = (
            PartialUser(data.get("user")) if data.get("user") else None
        )
        self.verify_key: str = data.get("verify_key")
        self.team: Optional[Team] = Team(data.get("team")) if data.get("get") else None
        self.cover_image: Optional[str] = data.get("cover_image")
        self.flags: int = data.get("flags")


class ApplicationCommand:
    def __init__(self, data: dict):
        self.id: str = data.get("id")
        self.type: int = data.get("type")
        self.application_id: str = data.get("application_id")
        self.guild_id: Optional[str] = data.get("guild_id")
        self.name: str = data.get("name")
        self.description: str = data.get("description")
        self.default_permissions: bool = data.get("default_permissions")
        self.version: str = data.get("version")


class GuildApplicationCommandPermission:
    def __init__(self, data: dict):
        self.id: str = data.get("id")
        self.application_id: str = data.get("application_id")
        self.guild_id: str = data.get("guild_id")
        self.permissions: ApplicationCommandPermission = ApplicationCommandPermission(
            data.get("permissions")
        )

    def to_dict(self):
        return {
            "id": self.id,
            "application_id": self.application_id,
            "guild_id": self.guild_id,
            "permissions": self.permissions.to_dict(),
        }


class ApplicationCommandPermission:
    def __init__(self, data: dict):
        self.id: str = data.get("id")
        self.type: int = data.get("type")
        self.permission: bool = data.get("permission")

    def to_dict(self):
        return {"id": self.id, "type": self.type, "permission": self.permission}


class ClientApplication(Application):
    def __init__(self, client, data: dict):
        super().__init__(data)
        self.client = client

    async def fetch_application(self):
        response: ClientResponse = await self.client.http.get("oauth2/applications/@me")
        data: dict = await response.json()
        return Application(data)

    async def fetch_global_application_commands(self) -> List[ApplicationCommand]:
        response = await self.client.http.get(f"/applications/{self.id}/commands")
        payload = [ApplicationCommand(command) for command in await response.json()]
        self.client.application_commands = payload
        return payload

    async def create_global_application_command(
        self,
        *,
        name: str,
        description: str,
        options: Optional[List[AnyOption]],
        default_permission: Optional[bool] = False,
        command_type: Optional[int] = 1,
    ):
        payload = {
            "name": name,
            "description": description,
            "default_permissions": default_permission,
        }

        if command_type not in range(1, 4):
            raise InvalidApplicationCommandType("Command type must be 1, 2, or 3.")

        payload["type"] = command_type

        for option in options:
            if not isinstance(
                option,
                (
                    Subcommand,
                    SubCommandGroup,
                    StringOption,
                    IntegerOption,
                    BooleanOption,
                    UserOption,
                    ChannelOption,
                    RoleOption,
                    MentionableOption,
                    NumberOption.AttachmentOption,
                ),
            ):
                raise InvalidApplicationCommandOptionType(
                    f"Options must be of type Subcommand, SubCommandGroup, "
                    f"StringOption, IntegerOption, BooleanOption, UserOption, "
                    f"ChannelOption, RoleOption, MentionableOption, "
                    f"NumberOption, not {option.__class__}. "
                )

        response = await self.client.http.post(
            f"/applications/{self.id}/commands", json=payload
        )
        return ApplicationCommand(await response.json())

    async def fetch_application_command(self, command_id: str):
        response = await self.client.http.get(
            f"/applications/{self.id}/commands/{command_id}"
        )
        return ApplicationCommand(await response.json())

    async def edit_global_application_command(
        self,
        command_id: str,
        *,
        name: Optional[str] = None,
        description: Optional[str] = None,
        options: Optional[List[AnyOption]] = None,
        default_permissions: Optional[bool] = None,
    ):
        payload = {}
        if name:
            payload["name"] = name
        if description:
            payload["description"] = description
        if options:
            payload["options"] = [option.to_dict() for option in options]
        if default_permissions:
            payload["default_permissions"] = default_permissions

        await self.client.http.patch(
            f"/applications/{self.id}/commands/{command_id}", json=payload
        )

    async def delete_global_application_command(self, command_id: str):
        await self.client.http.delete(f"/applications/{self.id}/commands/{command_id}")

    async def bulk_overwrite_global_application_commands(self, commands: List[Dict]):
        await self.client.http.put(f"/applications/{self.id}/commands", json=commands)

    async def fetch_guild_application_commands(self, guild_id: str):
        response = await self.client.http.get(
            f"/applications/{self.id}/guilds/{guild_id}/commands"
        )
        return [ApplicationCommand(command) for command in await response.json()]

    async def create_guild_application_command(
        self,
        guild_id: str,
        *,
        name: str,
        description: str,
        options=None,
        default_permission: Optional[bool] = False,
        command_type: Optional[int] = 1,
    ):
        if options is None:
            options = []

        payload = {
            "name": name,
            "description": description,
            "default_permissions": default_permission,
        }

        if command_type not in range(1, 4):
            raise InvalidApplicationCommandType("Command type must be 1, 2, or 3.")

        payload["type"] = command_type

        for option in options:
            if not isinstance(
                option,
                (
                    Subcommand,
                    SubCommandGroup,
                    StringOption,
                    IntegerOption,
                    BooleanOption,
                    UserOption,
                    ChannelOption,
                    RoleOption,
                    MentionableOption,
                    NumberOption.AttachmentOption,
                ),
            ):
                raise InvalidApplicationCommandOptionType(
                    f"Options must be of type Subcommand, SubCommandGroup, "
                    f"StringOption, IntegerOption, BooleanOption, UserOption, "
                    f"ChannelOption, RoleOption, MentionableOption, "
                    f"NumberOption, not {option.__class__}. "
                )

        response = await self.client.http.post(
            f"/applications/{self.id}/guilds/{guild_id}/commands", json=payload
        )
        return ApplicationCommand(await response.json())

    async def fetch_guild_application_command(self, guild_id: str, command_id: str):
        response = await self.client.http.get(
            f"/applications/{self.id}/guilds/{guild_id}/commands/{command_id}"
        )
        return ApplicationCommand(await response.json())

    async def edit_global_application_command(
        self,
        guild_id: str,
        command_id: str,
        *,
        name: Optional[str] = None,
        description: Optional[str] = None,
        options: Optional[List[AnyOption]] = None,
        default_permissions: Optional[bool] = None,
    ):
        payload = {}
        if name:
            payload["name"] = name
        if description:
            payload["description"] = description
        if options:
            payload["options"] = [option.to_dict() for option in options]
        if default_permissions:
            payload["default_permissions"] = default_permissions

        await self.client.http.patch(
            f"/applications/{self.id}/guilds/{guild_id}/commands/{command_id}",
            json=payload,
        )

    async def delete_guild_application_command(self, guild_id: str, command_id: str):
        await self.client.http.delete(
            f"/applications/{self.id}/guilds/{guild_id}/commands/{command_id}"
        )

    async def bulk_overwrite_guild_application_commands(
        self, guild_id: str, commands: List[Dict]
    ):
        await self.client.http.put(
            f"/applications/{self.id}/guilds/{guild_id}/commands", json=commands
        )

    async def fetch_guild_application_command_permissions(
        self, guild_id: str, command_id: str
    ):
        response = await self.client.http.get(
            f"/applications/{self.id}/guilds/{guild_id}/commands/{command_id}/permissions"
        )
        return [
            GuildApplicationCommandPermission(command)
            for command in await response.json()
        ]

    async def edit_application_command_permissions(
        self,
        guild_id: str,
        command_id,
        *,
        permissions: List[ApplicationCommandPermission],
    ):
        payload = [permission.to_dict() for permission in permissions]
        await self.client.http.put(
            f"/applications/{self.id}/guilds/{guild_id}/commands/{command_id}/permissions",
            json=payload,
        )


class Attachment:
    def __init__(self, data: dict):
        self.id: str = data.get("id")
        self.file_name: str = data.get("filename")
        self.description: Optional[str] = data.get("description")
        self.content_type: Optional[str] = data.get("content_type")
        self.size: int = data.get("size")
        self.url: str = data.get("url")
        self.proxy_url: str = data.get("proxy_url")
        self.width: Optional[int] = data.get("width")
        self.height: Optional[int] = data.get("height")
        self.ephemeral: Optional[bool] = data.get("ephemeral")


class BaseChannel:
    def __init__(self, client, data: dict):
        self.id: str = data.get("id")
        self.client = client
        self.type = data.get("type")


class GuildChannel(BaseChannel):
    def __init__(self, client, data: dict):
        super().__init__(client, data)
        self.guild_id: str = data.get("guild_id")
        self.position: int = data.get("position")
        self.nsfw: bool = data.get("nsfw")
        self.permission_overwrites: List[dict] = data.get("permission_overwrites")
        self.parent_id: str = data.get("parent_id")
        self.name: str = data.get("name")

    async def delete(self, *, reason: Optional[str] = None) -> None:
        if reason:
            headers = self.client.http.headers.copy()
        if reason:
            headers["reason"] = reason

        response = await self.client.http.delete(
            f"/channels/{self.id}", headers=headers, channel_id=self.id
        )
        return await response.json()

    async def fetch_invites(self):
        response = await self.client.http.get(
            f"/channels/{self.id}/invites", channel_id=self.id
        )
        return await response.json()

    async def create_invite(
        self,
        *,
        max_age: Optional[int],
        max_uses: Optional[int],
        temporary: Optional[bool],
        unique: Optional[bool],
        target_type: Optional[int],
        target_user_id: Optional[str],
        target_application_id: Optional[str],
    ):
        data = {
            "max_age": max_age or None,
            "max_uses": max_uses or None,
            "temporary": temporary or None,
            "unique": unique or None,
            "target_type": target_type or None,
            "target_user_id": target_user_id or None,
            "target_application_id": target_application_id or None,
        }

        await self.client.http.post(
            f"/channels/{self.id}/invites", json=data, channel_id=self.id
        )

    async def delete_overwrite(self, overwrites: Overwrite) -> None:
        response = await self.client.http.delete(
            f"/channels/{self.id}/permissions/{overwrites.id}", channel_id=self.id
        )
        return await response.json()

    async def fetch_pinned_messages(self) -> List[Message]:
        response = await self.client.http.get(
            f"/channels/{self.id}/pins", channel_id=self.id
        )
        data = await response.json()
        return [Message(self.client, message) for message in data]

    # async def edit_permission_overwrites I'll do this later

    # async def edit(self, *,name: str, position: str, permission_overwrites: List[dict], reason: Optional[str] = None):
    #     data = {}
    #     if name:
    #         data["name"] = name
    #     if position:
    #         data["position"] = position
    #     if permission_overwrites:
    #         data["permission_overwrites"] = permission_overwrites
    #     headers = self.client.http.headers
    #     headers["X-Audit-Log-Reason"] = reason
    #     response = await self.client.http.patch(f"channels/{self.id}", data=data, headers=headers)
    #     data = await response.json()
    #     return GuildChannel(self.client, data)


class TypingContextManager:
    def __init__(self, client, channel_id):
        self.typing: asyncio.Task = None
        self.client = client
        self.channel_id: str = channel_id

    async def start_typing(self):

        await self.client.http.post(f"/channels/{self.channel_id}/typing")
        asyncio.get_event_loop().call_later(10, self.start_typing)

    async def __aenter__(self):
        self.typing = asyncio.create_task(self.start_typing())

    async def __aexit__(self):
        self.typing.cancel()


class GuildTextChannel(GuildChannel, Messageable):
    def __init__(self, client, data: dict):
        super().__init__(client, data)
        self.topic: str = data.get("topic")
        self.rate_limit_per_user: int = data.get("rate_limit_per_user")
        self.last_message_id: str = data.get("last_message_id")
        self.default_auto_archive_duration: int = data.get(
            "default_auto_archive_duration"
        )

    async def start_thread(
        self,
        name: str,
        *,
        auto_archive_duration: Optional[int],
        type: Optional[int],
        invitable: Optional[bool],
        rate_limit_per_user: Optional[int],
        reason: Optional[str],
    ):
        data = {"name": name}
        if auto_archive_duration:
            data["auto_archive_duration"] = auto_archive_duration
        if type:
            data["type"] = type
        if invitable is not None:  # Geez having a bool is gonna be a pain
            data["invitable"] = invitable
        if rate_limit_per_user:
            data["rate_limit_per_user"] = rate_limit_per_user

        headers = self.client.http.headers.copy()

        if reason:
            headers["X-Audit-Log-Reason"] = reason

        response = await self.client.http.post(
            f"/channels/{self.id}/threads",
            data=data,
            headers=headers,
            channel_id=self.id,
        )
        self.client.guilds[self.guild_id].append(Thread(await response.json()))

    async def bulk_delete(self, message_ids: List[str], reason: Optional[str]) -> None:

        if reason:
            headers = self.client.http.headers.copy()
            headers["X-Audit-Log-Reason"] = reason

        response = await self.client.http.post(
            f"channels/{self.id}/messages/bulk-delete",
            data={"messages": message_ids},
            headers=headers,
            channel_id=self.id,
        )
        return await response.json()

    # It returns a List of Threads but I can't typehint that...
    async def list_public_archived_threads(
        self, *, before: Optional[str] = None, limit: Optional[int] = None
    ) -> Dict[str, Union[List[Messageable], List[ThreadMember], bool]]:

        params = {}

        if before:
            params["before"] = before

        if limit is not None:
            params["limit"] = limit

        response = await self.client.http.get(
            f"/channels/{self.id}/threads/archived/public",
            params=params,
            channel_id=self.id,
        )
        return await response.json()

    # It returns a List of Threads but I can't typehint that...
    async def list_private_archived_threads(
        self, *, before: Optional[str], limit: Optional[int]
    ) -> Dict[str, Union[List[Messageable], List[ThreadMember], bool]]:
        params = {}

        if before:
            params["before"] = before

        if limit is not None:
            params["limit"] = limit

        response = await self.client.http.get(
            f"/channels/{self.id}/threads/archived/private",
            params=params,
            channel_id=self.id,
        )
        return await response.json()

    async def list_joined_private_archived_threads(
        self, *, before: Optional[str], limit: Optional[int]
    ) -> Dict[str, Union[List[Messageable], List[ThreadMember], bool]]:
        params = {}

        if before:
            params["before"] = before

        if limit is not None:
            params["limit"] = limit

        response = await self.client.http.get(
            f"/channels/{self.id}/threads/archived/private",
            params=params,
            channel_id=self.id,
        )
        return await response.json()

    # async def edit(self,*, name: Optional[str], position: Optional[str], permission_overwrites: Optional[List[dict]], reason: Optional[str], topic: Optional[str], nsfw: bool, rate_limit_per_user: Optional[int], parent_id: Optional[int], default_auto_archive_duration: Optional[int]):
    #     data = {}
    #     if name:
    #         data["name"] = name
    #     if position:
    #         data["position"] = position
    #     if permission_overwrites:
    #         data["permission_overwrites"] = permission_overwrites

    #     headers = self.client.http.headers
    #     headers["X-Audit-Log-Reason"] = reason
    #     response = await self.client.http.patch(f"channels/{self.id}", data=data, headers=headers)
    #     data = await response.json()
    #     return GuildTextChannel(self.client, data)


class GuildNewsChannel(GuildTextChannel):
    def __init__(self, client, data: dict):
        super().__init__(client, data)
        self.default_auto_archive_duration: int = data.get(
            "default_auto_archive_duration"
        )

    async def follow(self, webhook_channel_id: str):
        response = await self.client.http.post(
            f"/channels/{self.id}/followers",
            json={"webhook_channel_id": webhook_channel_id},
            channel_id=self.id,
        )
        return await response.json()


class DMChannel(BaseChannel):
    def __init__(self, client, data: dict):
        super().__init__(client, data)
        self.recipient: Optional[List[PartialUser]] = (
            PartialUser(data.get("recipient")) if data.get("recipient") else None
        )


class ChannelCategory(GuildChannel):
    def __init__(self, client, data: dict):
        super().__init__(client, data)


class GuildNewsThread(Thread, GuildNewsChannel):
    def __init__(self, client, data: dict):
        super().__init__(client, data)


class GuildStageChannel(BaseChannel):
    def __init__(self, client, data: dict):
        super().__init__(client, data)
        self.guild_id: str = data.get("guild_id")
        self.channel_id: str = data.get("channel_id")
        self.privacy_level: int = data.get("privacy_level")
        self.discoverable_disabled: bool = data.get("discoverable_disabled")


class _FakeTask:
    def cancel(self):
        return True


class Bucket:
    def __init__(self, *, discord_hash: str):
        self.bucket_hash = discord_hash
        self.lock: asyncio.Lock = asyncio.Lock()

        self.close_task = _FakeTask()

    def __eq__(self, other):
        return self.bucket_hash == other.bucket_hash


class UnknownBucket:
    def __init__(self):
        self.lock = asyncio.Lock()
        self.close_task: _FakeTask = _FakeTask()


class DiscordWSMessage:
    def __init__(self, *, data, type, extra):
        self.data = data
        self.type = type
        self.extra = extra

    def json(self) -> Any:
        return json.loads(self.data)


class DiscordGatewayWebsocket(ClientWebSocketResponse):
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

    async def __anext__(self) -> dict:
        return await super().__anext__()


class HTTPClient(ClientSession):
    def __init__(self, *args, **kwargs):
        self.base_uri: str = kwargs.pop(
            "discord_endpoint", "https://discord.com/api/v10"
        )
        super().__init__(
            *args,
            **kwargs,
            json_serialize=lambda x, *__, **___: json.dumps(x).decode()
            if _ORJSON
            else json.dumps(x),
            ws_response_class=DiscordGatewayWebsocket,
        )
        self.global_ratelimit: asyncio.Event = asyncio.Event()
        self.global_ratelimit.set()
        self.buckets: Dict[str, Bucket] = {}

    async def request(self, method, url, *args, attempt: int = 1, **kwargs):

        if attempt > 5:
            logger.critical(f"Failed a {method} {url} 5 times.")
            return  # Just quit the request

        if url.startswith("ws"):
            return await super().request(method, url, *args, **kwargs)

        if url.startswith("/"):
            url = url[1:]

        if url.endswith("/"):
            url = url[: len(url) - 1]

        url = f"{self.base_uri}/{url}"

        await self.global_ratelimit.wait()

        guild_id: Union[str, int] = kwargs.get("guild_id", 0)
        channel_id: Union[str, int] = kwargs.get("channel_id", 0)
        bucket_hash = f"{guild_id}:{channel_id}:{url}"
        bucket = self.buckets.get(bucket_hash)

        if not bucket:
            bucket = UnknownBucket()

        await bucket.lock.acquire()

        res = await super().request(method, url, *args, **kwargs)

        await self.log_request(res)

        if isinstance(bucket, UnknownBucket) and res.headers.get("X-RateLimit-Bucket"):
            if guild_id and channel_id:
                self.buckets[res.headers.get("X-RateLimit-Bucket")] = Bucket(
                    discord_hash=res.headers.get("X-RateLimit-Bucket")
                )
            else:
                b = Bucket(discord_hash=res.headers.get("X-RateLimit-Bucket"))
                if b in self.buckets.values():
                    self.buckets[bucket_hash] = {v: k for k, v in self.buckets.items()}[
                        b
                    ]
                else:
                    self.buckets[bucket_hash] = b
        body = {}
        if res.headers["Content-Type"] == "application/json":
            body = await res.json()
        else:
            body = await res.text()
        if (
            int(res.headers.get("X-RateLimit-Remaining", 1)) == 0
            and res.status != HTTPCodes.TOO_MANY_REQUESTS
        ):  # We've exhausted the bucket.
            logger.critical(
                f"Exhausted {res.headers['X-RateLimit-Bucket']} ({res.url}). Reset in {res.headers['X-RateLimit-Reset-After']} seconds"
            )
            await asyncio.sleep(float(res.headers["X-RateLimit-Reset-After"]))
            bucket.lock.release()

        if res.status == HTTPCodes.TOO_MANY_REQUESTS:  # Body is always present here.
            time_to_sleep = (
                body.get("retry_after")
                if body.get("retry_after") > res.headers["X-RateLimit-Reset-After"]
                else res.headers["X-RateLimit-Reset-After"]
            )

            logger.critical(f"Rate limited. Reset in {time_to_sleep} seconds")
            if res.headers["X-RateLimit-Scope"] == "global":
                await self.global_ratelimit.clear()

            await asyncio.sleep(time_to_sleep)

            await self.global_ratelimit.set()
            bucket.lock.release()
            return await self.request(
                method, url, *args, **kwargs, attempt=attempt + 1
            )  # Retry the request

        if res.status >= HTTPCodes.SERVER_ERROR:
            raise DiscordServerError5xx(body)

        elif res.status == HTTPCodes.NOT_FOUND:
            raise NotFound404(body)

        elif res.status == HTTPCodes.FORBIDDEN:
            raise Forbidden403(body)

        elif not 300 > res.status >= 200:
            raise DiscordAPIError(body)

        if bucket.lock.locked():
            try:
                bucket.lock.release()
            except Exception as e:
                logger.exception(e)

        async def dispose():  # After waiting 5 minutes without any interaction, the bucket will be disposed.
            await asyncio.sleep(300)
            try:
                del self.buckets[bucket_hash]
            except KeyError:
                ...

        bucket.close_task.cancel()

        bucket.close_task = asyncio.get_event_loop().create_task(dispose())

        return res

    @staticmethod
    async def log_request(res):
        message = [
            f"Sent a {res.request_info.method} to {res.url} "
            f"and got a {res.status} response. ",
            f"Content-Type: {res.headers['Content-Type']} ",
        ]

        if h := dict(res.headers):
            message.append(f"Received headers: {h} ")

        if h := dict(res.request_info.headers):
            message.append(f"Sent headers: {h} ")

        try:
            await res.json()
            message.append(f"Received body: {await res.json()} ")

        finally:
            logger.debug("".join(message))

    async def get(
        self,
        url,
        *args,
        to_discord: bool = True,
        **kwargs,
    ):
        if to_discord:
            res = await self.request("GET", url, *args, **kwargs)
            return res

        return await super().get(url, *args, **kwargs)

    async def post(self, url, *args, to_discord: bool = True, **kwargs):
        if to_discord:
            res = await self.request("POST", url, *args, **kwargs)
            return res

        return await self.post(url, *args, **kwargs)

    async def patch(self, url, *args, to_discord: bool = True, **kwargs):
        if to_discord:
            res = await self.request("PATCH", url, *args, **kwargs)
            return res
        return await super().patch(url, *args, **kwargs)

    async def delete(self, url, *args, to_discord: bool = True, **kwargs):
        if to_discord:
            res = await self.request("DELETE", url, *args, **kwargs)
            return res
        return await super().delete(url, **kwargs)

    async def put(self, url, *args, to_discord: bool = True, **kwargs):
        if to_discord:
            res = await self.request("PUT", url, *args, **kwargs)
            return res
        return await super().put(url, *args, **kwargs)


class Event:
    def __init__(self, callback, *, event_name: str):
        self.callback = callback
        self.event_name = event_name or callback.__name__


class Section:
    _commands: Dict[
        str, Union[ClientUserCommand, ClientSlashCommand, ClientMessageCommand]
    ] = defaultdict(list)
    _events: Dict[str, Event] = defaultdict(list)

    def __init_subclass__(cls, **kwargs):
        for attr_value in cls.__dict__.values():
            if isinstance(attr_value, Event):
                cls._events[cls.__name__].append(attr_value)

            elif issubclass(
                attr_value,
                (ClientSlashCommand, ClientUserCommand, ClientMessageCommand),
            ):
                cls._commands[cls.__name__].append(attr_value)

        super().__init_subclass__(**kwargs)


class Client(WebsocketClient):
    def __init__(
        self,
        token: str,
        intents: int = 0,
        *,
        status: Optional[Status] = None,
        activity: Optional[Activity] = None,
        overwrite_commands_on_ready: Optional[bool] = False,
        discord_endpoint: str = "https://discord.com/api/v10",
    ):
        super().__init__(token, intents)
        self.overwrite_commands_on_ready: bool = overwrite_commands_on_ready
        self.commands: Dict[
            str, Union[ClientSlashCommand, ClientUserCommand, ClientMessageCommand]
        ] = {}
        self.guilds: GuildManager = GuildManager(self)
        self.channels: ChannelManager = ChannelManager(self)
        self.presence: Presence = Presence(status=status, activity=activity)
        self._components = {}

        self.http: HTTPClient = HTTPClient(
            headers={
                "Authorization": f"Bot {token}",
                "User-Agent": f"DiscordBot (https://github.com/EpikCord/EpikCord.py {__version__})",
            },
            discord_endpoint=discord_endpoint,
        )

        self.utils = Utils(self)
        self.latencies = deque(maxlen=5)
        self.user: ClientUser = None
        self.application: Optional[ClientApplication] = None
        self.sections: List[Any] = []

    @property
    def latency(self):
        return self.discord_latency

    @property
    def average_latency(self):
        return sum(self.latencies) / len(self.latencies)

    def command(
        self,
        *,
        name: Optional[str] = None,
        description: str = None,
        guild_ids: Optional[List[str]] = None,
        options: Optional[List[AnyOption]] = None,
        name_localizations: Optional[List[Localization]] = None,
        description_localizations: Optional[List[Localization]] = None,
        name_localisations: Optional[List[Localisation]] = None,
        description_localisations: Optional[List[Localisation]] = None,
    ):
        name_localization = self.utils.match_mixed(
            name_localizations, name_localisations
        )
        description_localization = self.utils.match_mixed(
            description_localizations, description_localisations
        )

        def register_slash_command(func):
            desc = description or func.__doc__
            if not desc:
                raise TypeError(
                    f"Command with {name or func.__name__} has no description. This is required."
                )

            command = ClientSlashCommand(
                name=name or func.__name__,
                description=desc,
                guild_ids=guild_ids or [],
                options=options or [],
                callback=func,
                name_localization=name_localization,
                description_localization=description_localization,
            )

            self.commands[command.name] = command
            return command

        return register_slash_command

    def user_command(self, name: Optional[str] = None):
        def register_slash_command(func):
            result = ClientUserCommand(
                **{
                    "callback": func,
                    "name": name or func.__name__,
                }
            )
            self.commands[name](result)
            return result

        return register_slash_command

    def message_command(self, name: Optional[str] = None):
        def register_slash_command(func):
            self.commands[name] = ClientMessageCommand(
                **{
                    "callback": func,
                    "name": name or func.__name__,
                }
            )

        return register_slash_command

    def add_check(self, check: "Check"):
        def wrapper(command_callback):
            command = list(
                filter(lambda c: c.callback == command_callback, self.commands.values())
            )
            command[0].checks.append(check)

        return wrapper

    def load_section(self, section: Section):

        for event in section._events.values():
            self.events[event.name] = event.callback

        for command in section._commands.values():
            self.commands[command.name] = command

        logger.info(f"Loaded Section {section.__name__}")

    def load_sections_from_file(self, filename: str):
        sections = import_module(filename)

        for possible_section in sections.__dict__.values():
            if issubclass(possible_section, Section):
                self.load_section(possible_section)


# class ClientGuildMember(Member):
#     def __init__(self, client: Client,data: dict):
#         super().__init__(data)


class Colour:
    # Some of this code is sourced from discord.py, rest assured all the
    # colors are different from discord.py
    __slots__ = ("value",)

    def __init__(self, value: int):
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int parameter, received {value.__class__.__name__} instead."
            )

        self.value: int = value

    def _get_byte(self, byte: int) -> int:
        return (self.value >> (8 * byte)) & 0xFF

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Colour) and self.value == other.value

    def __ne__(self, other: Any) -> bool:
        return not self.__eq__(other)

    def __str__(self) -> str:
        return f"#{self.value:0>6x}"

    def __int__(self) -> int:
        return self.value

    def __repr__(self) -> str:
        return f"<Colour value={self.value}>"

    def __hash__(self) -> int:
        return hash(self.value)

    @property
    def r(self) -> int:
        """Return the red component in rgb"""
        return self._get_byte(2)

    @property
    def g(self) -> int:
        """Return the green component in rgb"""
        return self._get_byte(1)

    @property
    def b(self) -> int:
        """Return the blue component in rgb"""
        return self._get_byte(0)

    def to_rgb(self) -> Tuple[int, int, int]:
        """Returns a rgb color as a tuple"""
        return self.r, self.g, self.b

    @classmethod
    def from_rgb(cls: Type[CT], r: int, g: int, b: int) -> CT:
        """Constructs a :class:`Colour` from an RGB tuple."""
        return cls((r << 16) + (g << 8) + b)

    @classmethod
    def lime_green(cls: Type[CT]) -> CT:
        """Returns a color of lime green"""
        return cls(0x00FF01)

    @classmethod
    def light_green(cls: Type[CT]) -> CT:
        """Returns a color of light green"""
        return cls(0x00FF22)

    @classmethod
    def dark_green(cls: Type[CT]) -> CT:
        """Returns a color of dark green"""
        return cls(0x00570A)

    @classmethod
    def light_blue(cls: Type[CT]) -> CT:
        """Returns a color of light blue"""
        return cls(0x00FF01)

    @classmethod
    def dark_blue(cls: Type[CT]) -> CT:
        """Returns a color of dark blue"""
        return cls(0x0A134B)

    @classmethod
    def light_red(cls: Type[CT]) -> CT:
        """Returns a color of light red"""
        return cls(0xAA5B54)

    @classmethod
    def dark_red(cls: Type[CT]) -> CT:
        """Returns a color of dark red"""
        return cls(0x4C0000)

    @classmethod
    def black(cls: Type[CT]) -> CT:
        """Returns a color of black"""
        return cls(0x000000)

    @classmethod
    def white(cls: Type[CT]) -> CT:
        """Returns a color of white"""
        return cls(0xFFFFFF)

    @classmethod
    def lightmode(cls: Type[CT]) -> CT:
        """Returns the color of the background when the color theme in
        Discord is set to light mode. An alias of `white`"""
        return cls(0xFFFFFF)

    @classmethod
    def darkmode(cls: Type[CT]) -> CT:
        """Returns the color of the background when the color theme in
        Discord is set to dark mode"""
        return cls(0x363940)

    @classmethod
    def amoled(cls: Type[CT]) -> CT:
        """Returns the color of the background when the color theme in
        Discord is set to amoled mode. An alias of `black`"""
        return cls(0x000000)

    @classmethod
    def blurple_old(cls: Type[CT]) -> CT:
        """Returns the old Discord Blurple color"""
        return cls(0x7289DA)

    @classmethod
    def blurple_new(cls: Type[CT]) -> CT:
        """Returns the new Discord Blurple color"""
        return cls(0x5865F2)

    default = black


Color = Colour


class Embed:  # Always wanted to make this class :D
    def __init__(
        self,
        *,
        title: Optional[str] = None,
        description: Optional[str] = None,
        color: Optional[Colour] = None,
        video: Optional[dict] = None,
        timestamp: Optional[datetime.datetime] = None,
        colour: Optional[Colour] = None,
        url: Optional[str] = None,
        type: Optional[int] = None,
        footer: Optional[dict] = None,
        image: Optional[dict] = None,
        thumbnail: Optional[dict] = None,
        provider: Optional[dict] = None,
        author: Optional[dict] = None,
        fields: Optional[List[dict]] = None,
    ):
        self.type: int = type
        self.title: Optional[str] = title
        self.type: Optional[str] = type
        self.description: Optional[str] = description
        self.url: Optional[str] = url
        self.video: Optional[dict] = video
        self.timestamp: Optional[str] = timestamp
        self.color: Optional[Colour] = color or colour
        self.footer: Optional[str] = footer
        self.image: Optional[str] = image
        self.thumbnail: Optional[str] = thumbnail
        self.provider: Optional[str] = provider
        self.author: Optional[dict] = author
        self.fields: Optional[List[str]] = fields

    def add_field(self, *, name: str, value: str, inline: bool = False):
        self.fields.append({"name": name, "value": value, "inline": inline})

    def set_thumbnail(
        self,
        *,
        url: Optional[str] = None,
        proxy_url: Optional[str] = None,
        height: Optional[int] = None,
        width: Optional[int] = None,
    ):
        config = {"url": url}
        if proxy_url:
            config["proxy_url"] = proxy_url
        if height:
            config["height"] = height
        if width:
            config["width"] = width

        self.thumbnail = config

    def set_video(
        self,
        *,
        url: Optional[str] = None,
        proxy_url: Optional[str] = None,
        height: Optional[int] = None,
        width: Optional[int] = None,
    ):
        config = {"url": url}
        if proxy_url:
            config["proxy_url"] = proxy_url
        if height:
            config["height"] = height
        if width:
            config["width"] = width

        self.video = config

    def set_image(
        self,
        *,
        url: Optional[str] = None,
        proxy_url: Optional[str] = None,
        height: Optional[int] = None,
        width: Optional[int] = None,
    ):
        config = {"url": url}
        if proxy_url:
            config["proxy_url"] = proxy_url
        if height:
            config["height"] = height
        if width:
            config["width"] = width

        self.image = config

    def set_provider(self, *, name: Optional[str] = None, url: Optional[str] = None):
        config = {}
        if url:
            config["url"] = url
        if name:
            config["name"] = name
        self.provider = config

    def set_footer(
        self,
        *,
        text: Optional[str],
        icon_url: Optional[str] = None,
        proxy_icon_url: Optional[str] = None,
    ):
        payload = {}
        if text:
            payload["text"] = text
        if icon_url:
            payload["icon_url"] = icon_url
        if proxy_icon_url:
            payload["proxy_icon_url"] = proxy_icon_url
        self.footer = payload

    def set_author(
        self,
        name: Optional[str] = None,
        url: Optional[str] = None,
        icon_url: Optional[str] = None,
        proxy_icon_url: Optional[str] = None,
    ):
        payload = {}
        if name:
            payload["name"] = name
        if url:
            payload["url"] = url
        if icon_url:
            payload["icon_url"] = icon_url
        if proxy_icon_url:
            payload["proxy_icon_url"] = proxy_icon_url

        self.author = payload

    def set_fields(self, *, fields: List[dict]):
        self.fields = fields

    def set_color(self, *, colour: Colour):
        self.color = colour.value

    def set_timestamp(self, *, timestamp: datetime.datetime):
        self.timestamp = timestamp.isoformat()

    def set_title(self, title: Optional[str] = None):
        self.title = title

    def set_description(self, description: Optional[str] = None):
        self.description = description

    def set_url(self, url: Optional[str] = None):
        self.url = url

    def to_dict(self):
        final_product = {}

        if hasattr(self, "title"):
            final_product["title"] = self.title
        if hasattr(self, "description"):
            final_product["description"] = self.description
        if hasattr(self, "url"):
            final_product["url"] = self.url
        if hasattr(self, "timestamp"):
            final_product["timestamp"] = self.timestamp
        if hasattr(self, "color"):
            final_product["color"] = self.color.value
        if hasattr(self, "footer"):
            final_product["footer"] = self.footer
        if hasattr(self, "image"):
            final_product["image"] = self.image
        if hasattr(self, "thumbnail"):
            final_product["thumbnail"] = self.thumbnail
        if hasattr(self, "video"):
            final_product["video"] = self.video
        if hasattr(self, "provider"):
            final_product["provider"] = self.provider
        if hasattr(self, "author"):
            final_product["author"] = self.author
        if hasattr(self, "fields"):
            final_product["fields"] = self.fields

        return final_product


class RoleTag:
    def __init__(self, data: dict):
        self.bot_id: Optional[str] = data.get("bot_id")
        self.integration_id: Optional[str] = data.get("integration_id")
        self.premium_subscriber: Optional[bool] = data.get("premium_subscriber")


class Role:
    def __init__(self, client, data: dict):
        self.data = data
        self.client = client
        self.id: str = data.get("id")
        self.name: str = data.get("name")
        self.color: int = data.get("color")
        self.hoist: bool = data.get("hoist")
        self.icon: Optional[str] = data.get("icon")
        self.unicode_emoji: Optional[str] = data.get("unicode_emoji")
        self.position: int = data.get("position")
        self.permissions: str = data.get("permissions")  # TODO: Permissions
        self.managed: bool = data.get("managed")
        self.mentionable: bool = data.get("mentionable")
        self.tags: RoleTag = RoleTag(self.data.get("tags"))
        self.guild: Guild = data.get("guild")


class Emoji:
    def __init__(self, client, data: dict, guild_id: str):
        self.client = client
        self.id: Optional[str] = data.get("id")
        self.name: Optional[str] = data.get("name")
        self.roles: List[Role] = [
            Role(client, role)
            for role in [
                {**role_data, "guild": self} for role_data in data.get("roles")
            ]
        ]
        self.user: Optional[User] = User(data.get("user")) if data.get("user") else None
        self.requires_colons: bool = data.get("require_colons")
        self.guild_id: str = data.get("guild_id")
        self.managed: bool = data.get("managed")
        self.guild_id: str = guild_id
        self.animated: bool = data.get("animated")
        self.available: bool = data.get("available")

    async def edit(
        self,
        *,
        name: Optional[str] = None,
        roles: Optional[List[Role]] = None,
        reason: Optional[str] = None,
    ):
        payload = {}
        headers = self.client.http.headers.copy()
        if reason:
            headers["X-Audit-Log-Reason"] = reason

        if name:
            payload["name"] = name

        if roles:
            payload["roles"] = [role.id for role in roles]

        emoji = await self.client.http.patch(
            f"/guilds/{self.guild_id}/emojis/{self.id}", json=payload, headers=headers
        )
        return Emoji(self.client, emoji, self.guild_id)

    async def delete(self, *, reason: Optional[str] = None):
        headers = self.client.http.headers.copy()
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        await self.client.http.delete(
            f"/guilds/{self.guild_id}/emojis/{self.id}", headers=headers
        )


class WelcomeScreenChannel:
    def __init__(self, data: dict):
        self.channel_id: str = data.get("channel_id")
        self.description: str = data.get("description")
        self.emoji_id: Optional[str] = data.get("emoji_id")
        self.emoji_name: Optional[str] = data.get("emoji_name")


class WelcomeScreen:
    def __init__(self, data: dict):
        self.description: Optional[str] = data.get("description")
        self.welcome_channels: List[WelcomeScreenChannel] = [
            WelcomeScreenChannel(welcome_channel)
            for welcome_channel in data.get("welcome_channels")
        ]


class GuildPreview:
    def __init__(self, data: dict):
        self.id: str = data.get("id")
        self.name: str = data.get("name")
        self.icon: Optional[str] = data.get("icon")
        self.splash: Optional[str] = data.get("splash")
        self.discovery_splash: Optional[str] = data.get("discovery_splash")
        self.emojis: List[Emoji] = [Emoji(emoji) for emoji in data.get("emojis", [])]
        self.features: List[str] = data.get("features")
        self.approximate_member_count: int = data.get("approximate_member_count")
        self.approximate_presence_count: int = data.get("approximate_presence_count")
        self.stickers: List[Sticker] = [
            Sticker(sticker) for sticker in data.get("stickers", [])
        ]


class GuildWidgetSettings:
    def __init__(self, data: dict):
        self.enabled: bool = data.get("enabled")
        self.channel_id: Optional[str] = data.get("channel_id")


class GuildWidget:
    def __init__(self, data: dict):
        self.id: str = data.get("id")
        self.name: str = data.get("name")
        self.instant_invite: str = data.get("instant_invite")
        self.channels: List[GuildChannel] = [
            GuildChannel(channel) for channel in data.get("channels", [])
        ]
        self.users: List[User] = [User(user) for user in data.get("members", [])]
        self.presence_count: int = data.get("presence_count")


class GuildScheduledEvent:
    def __init__(self, client: Client, data: dict):
        self.id: str = data.get("id")
        self.client = client
        self.guild_id: str = data.get("guild_id")
        self.channel_id: Optional[str] = data.get("channel_id")
        self.creator_id: Optional[str] = data.get("creator_id")
        self.name: str = data.get("name")
        self.description: Optional[str] = data.get("description")
        self.scheduled_start_time: str = data.get("scheduled_start_time")
        self.scheduled_end_time: Optional[str] = data.get("scheduled_end_time")
        self.privacy_level: int = data.get("privacy_level")
        self.status: str = (
            "SCHEDULED"
            if data.get("status") == 1
            else "ACTIVE"
            if data.get("status") == 2
            else "COMPLETED"
            if data.get("status") == 3
            else "CANCELLED"
        )
        self.entity_type: str = (
            "STAGE_INSTANCE"
            if data.get("entity_type") == 1
            else "VOICE"
            if data.get("entity_type") == 2
            else "EXTERNAL"
        )
        self.entity_id: str = data.get("entity_id")
        self.entity_metadata: dict = data.get("entity_metadata")
        self.creator: Optional[User] = User(data.get("creator"))
        self.user_count: Optional[int] = data.get("user_count")


class IntegrationAccount:
    def __init__(self, data: dict):
        self.id: str = data.get("id")
        self.name: str = data.get("name")


class GuildBan:
    def __init__(self, data: dict):
        self.reason: Optional[str] = data.get("reason")
        self.user: User = User(data.get("user"))


class Integration:
    def __init__(self, data: dict):
        self.id: str = data.get("id")
        self.name: str = data.get("name")
        self.type: str = data.get("type")
        self.enabled: bool = data.get("enabled")
        self.syncing: Optional[bool] = data.get("syncing")
        self.role_id: Optional[str] = data.get("role_id")
        self.expire_behavior: str = (
            "REMOVE_ROLE"
            if data.get("expire_behavior") == 1
            else "REMOVE_ACCOUNT"
            if data.get("expire_behavior") == 2
            else None
        )
        self.expire_grace_period: Optional[int] = data.get("expire_grace_period")
        self.user: Optional[User] = User(data.get("user")) if data.get("user") else None
        self.account: IntegrationAccount = IntegrationAccount(data.get("account"))
        self.synced_at: datetime.datetime = datetime.datetime.fromioformat(
            data.get("synced_at")
        )
        self.subscriber_count: int = data.get("subscriber_count")
        self.revoked: bool = data.get("revoked")
        self.application: Optional[Application] = (
            Application(data.get("application")) if data.get("application") else None
        )


class SystemChannelFlags:
    def __init__(self, *, value: Optional[int] = None):
        self.value: int = value

    @property
    def suppress_join_notifications(self):
        self.value += 1 << 0

    @property
    def suppress_premium_subscriptions(self):
        self.value += 1 << 1

    @property
    def suppress_guild_reminder_notifications(self):
        self.value += 1 << 2

    @property
    def suppress_join_notification_replies(self):
        self.value += 1 << 3


class Guild:
    def __init__(self, client: Client, data: dict):
        self.client = client
        self.lock: asyncio.Lock = asyncio.Lock()
        self.data: dict = data
        self.id: str = data.get("id")
        self.name: str = data.get("name")
        self.icon: Optional[str] = data.get("icon")
        self.http_lock: asyncio.Lock = asyncio.Lock()
        self.icon_hash: Optional[str] = data.get("icon_hash")
        self.splash: Optional[str] = data.get("splash")
        self.discovery_splash: Optional[str] = data.get("discovery_splash")
        self.owner_id: str = data.get("owner_id")
        self.permissions: str = data.get("permissions")
        self.afk_channel_id: str = data.get("afk_channel_id")
        self.afk_timeout: int = data.get("afk_timeout")

        levels = ["None", "Low", "Medium", "High", "Very High"]

        _lvl = min(data.get("verification_level"), len(levels) - 1)
        self.verification_level: str = levels[_lvl].upper()

        self.default_message_notifications: str = (
            "ALL" if data.get("default_message_notifications") == 0 else "MENTIONS"
        )
        self.explicit_content_filter: str = (
            "DISABLED"
            if data.get("explicit_content_filter") == 0
            else "MEMBERS_WITHOUT_ROLES"
            if data.get("explicit_content_filter") == 1
            else "ALL_MEMBERS"
        )
        self.roles: List[Role] = [
            Role(client, role)
            for role in [
                {**role_data, "guild": self} for role_data in data.get("roles")
            ]
        ]
        self.emojis: List[Emoji] = [
            Emoji(client, emoji, self.id) for emoji in data.get("emojis")
        ]
        self.features: List[str] = data.get("features")
        self.mfa_level: str = "NONE" if data.get("mfa_level") == 0 else "ELEVATED"
        self.application_id: Optional[str] = data.get("application_id")
        self.system_channel_id: Optional[str] = data.get("system_channel_id")
        self.system_channel_flags: int = data.get("system_channel_flags")
        self.rules_channel_id: Optional[int] = data.get("rules_channel_id")
        self.joined_at: Optional[str] = data.get("joined_at")
        self.large: bool = data.get("large")
        self.unavailable: bool = data.get("unavailable")
        self.member_count: int = data.get("member_count")
        # self.voice_states: List[dict] = data["voice_states"]
        self.members: List[GuildMember] = [
            GuildMember(client, member) for member in data.get("members")
        ]
        self.channels: List[GuildChannel] = [
            client.utils.channel_from_type(channel) for channel in data.get("channels")
        ]
        self.threads: List[Thread] = [Thread(thread) for thread in data.get("threads")]
        self.presences: List[dict] = data.get("presences")
        self.max_presences: int = data.get("max_presences")
        self.max_members: int = data.get("max_members")
        self.vanity_url_code: Optional[str] = data.get("vanity_url_code")
        self.description: Optional[str] = data.get("description")
        self.banner: Optional[str] = data.get("banner")
        self.premium_tier: int = data.get("premium_tier")
        self.premium_subscription_count: int = data.get("premium_subscription_count")
        self.preferred_locale: str = data.get("preferred_locale")
        self.public_updates_channel_id: Optional[str] = data.get(
            "public_updates_channel_id"
        )
        self.max_video_channel_users: Optional[int] = data.get(
            "max_video_channel_users"
        )
        self.approximate_member_count: Optional[int] = data.get(
            "approximate_member_count"
        )
        self.approximate_presence_count: Optional[int] = data.get(
            "approximate_presence_count"
        )
        self.welcome_screen: Optional[WelcomeScreen] = (
            WelcomeScreen(data.get("welcome_screen"))
            if data.get("welcome_screen")
            else None
        )
        self.nsfw_level: int = data.get("nsfw_level")
        self.stage_instances: List[GuildStageChannel] = [
            GuildStageChannel(client, channel)
            for channel in data.get("stage_instances")
        ]
        self.stickers: Optional[StickerItem] = (
            StickerItem(data.get("stickers")) if data.get("stickers") else None
        )
        self.guild_schedulded_events: List[GuildScheduledEvent] = [
            GuildScheduledEvent(client, event)
            for event in data.get("guild_schedulded_events", [])
        ]

    async def edit(
        self,
        *,
        name: Optional[str] = None,
        verification_level: Optional[int] = None,
        default_message_notifications: Optional[int] = None,
        explicit_content_filter: Optional[int] = None,
        afk_channel_id: Optional[str] = None,
        afk_timeout: Optional[int] = None,
        owner_id: Optional[str] = None,
        system_channel_id: Optional[str] = None,
        system_channel_flags: Optional[SystemChannelFlags] = None,
        rules_channel_id: Optional[str] = None,
        preferred_locale: Optional[str] = None,
        features: Optional[List[str]] = None,
        description: Optional[str] = None,
        premium_progress_bar_enabled: Optional[bool] = None,
        reason: Optional[str] = None,
    ):
        """Edits the guild.

        Parameters
        ----------
        name: Optional[str]
            The name of the guild.
        verification_level: Optional[int]
            The verification level of the guild.
        default_message_notifications: Optional[int]
            The default message notifications of the guild.
        explicit_content_filter: Optional[int]
            The explicit content filter of the guild.
        afk_channel_id: Optional[str]
            The afk channel id of the guild.
        afk_timeout: Optional[int]
            The afk timeout of the guild.
        owner_id: Optional[str]
            The owner id of the guild.
        system_channel_id: Optional[str]
            The system channel id of the guild.
        system_channel_flags: Optional[SystemChannelFlags]
            The system channel flags of the guild.
        rules_channel_id: Optional[str]
            The rules channel id of the guild.
        preferred_locale: Optional[str]
            The preferred locale of the guild.
        features: Optional[List[str]]
            The features of the guild.
        description: Optional[str]
            The description of the guild.
        premium_progress_bar_enabled: Optional[bool]
            Whether the guild has the premium progress bar enabled.

        Returns
        -------
        :class:`EpikCord.Guild`
        """
        data = {}
        if name is not None:
            data["name"] = name
        if verification_level is not None:
            data["verification_level"] = verification_level
        if default_message_notifications is not None:
            data["default_message_notifications"] = default_message_notifications
        if explicit_content_filter is not None:
            data["explicit_content_filter"] = explicit_content_filter
        if afk_channel_id is not None:
            data["afk_channel_id"] = afk_channel_id
        if afk_timeout is not None:
            data["afk_timeout"] = afk_timeout
        if owner_id is not None:
            data["owner_id"] = owner_id
        if system_channel_id is not None:
            data["system_channel_id"] = system_channel_id.value
        if system_channel_flags is not None:
            data["system_channel_flags"] = system_channel_flags
        if rules_channel_id is not None:
            data["rules_channel_id"] = rules_channel_id
        if preferred_locale is not None:
            data["preferred_locale"] = preferred_locale
        if features is not None:
            data["features"] = features
        if description is not None:
            data["description"] = description
        if premium_progress_bar_enabled is not None:
            data["premium_progress_bar_enabled"] = premium_progress_bar_enabled

        headers = self.client.http.headers.copy()
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        return Guild(
            await self.client.http.patch(
                f"/guilds/{self.id}", json=data, headers=headers, guild_id=self.id
            )
        )

    async def fetch_guild_preview(self) -> GuildPreview:
        """Fetches the guild preview.

        Returns
        -------
        GuildPreview
            The guild preview.
        """
        if getattr(self, "preview"):
            return self.preview

        res = await self.client.http.get(f"/guilds/{self.id}/preview", guild_id=self.id)

        data = await res.json()

        return GuildPreview(data)

    async def delete(self):
        await self.client.http.delete(f"/guilds/{self.id}", guild_id=self.id)

    async def fetch_channels(self) -> List[GuildChannel]:
        """Fetches the guild channels.

        Returns
        -------
        List[GuildChannel]
            The guild channels.
        """
        channels = await self.client.http.get(
            f"/guilds/{self.id}/channels", guild_id=self.id
        )
        return [self.client.utils.channel_from_type(channel) for channel in channels]

    async def create_channel(
        self,
        *,
        name: str,
        reason: Optional[str] = None,
        type: Optional[int] = None,
        topic: Optional[str] = None,
        bitrate: Optional[int] = None,
        user_limit: Optional[int] = None,
        rate_limit_per_user: Optional[int] = None,
        position: Optional[int] = None,
        permission_overwrites: List[Optional[Overwrite]] = None,
        parent_id: Optional[str] = None,
        nsfw: Optional[bool] = None,
    ):
        """Creates a channel.

        Parameters
        ----------
        name: str
            The name of the channel.
        reason: Optional[str]
            The reason for creating the channel.
        type: Optional[int]
            The type of the channel.
        topic: Optional[str]
            The topic of the channel.
        bitrate: Optional[int]
            The bitrate of the channel.
        user_limit: Optional[int]
            The user limit of the channel.
        rate_limit_per_user: Optional[int]
            The rate limit per user of the channel.
        position: Optional[int]
            The position of the channel.
        permission_overwrites: List[Optional[Overwrite]]
            The permission overwrites of the channel.
        parent_id: Optional[str]
            The parent id of the channel.
        nsfw: Optional[bool]
            Whether the channel is nsfw.
        """
        data = {}
        if name is not None:
            data["name"] = name
        if type is not None:
            data["type"] = type
        if topic is not None:
            data["topic"] = topic
        if bitrate is not None:
            data["bitrate"] = bitrate
        if user_limit is not None:
            data["user_limit"] = user_limit
        if rate_limit_per_user is not None:
            data["rate_limit_per_user"] = rate_limit_per_user
        if position is not None:
            data["position"] = position
        if permission_overwrites is not None:
            data["permission_overwrites"] = permission_overwrites
        if parent_id is not None:
            data["parent_id"] = parent_id
        if nsfw is not None:
            data["nsfw"] = nsfw

        headers = self.client.http.headers.copy()
        if reason:
            headers["X-Audit-Log-Reason"] = reason

        return self.client.utils.channel_from_type(
            await (
                await self.client.http.post(
                    f"/guilds/{self.id}/channels",
                    json=data,
                    headers=headers,
                    guild_id=self.id,
                )
            ).json()
        )


class WebhookUser:
    def __init__(self, data: dict):
        self.webhook_id: str = data.get("webhook_id")
        self.username: str = data.get("username")
        self.avatar: str = data.get("avatar")


class Webhook:
    def __init__(self, client, data: dict):
        self.client = client
        self.data = data
        if data:
            self.id: str = data.get("id")
            self.type: str = (
                "Incoming"
                if data.get("type") == 1
                else "Channel Follower"
                if data.get("type") == 2
                else "Application"
            )
            self.guild_id: Optional[str] = data.get("guild_id")
            self.channel_id: Optional[str] = data.get("channel_id")
            self.user: Optional[User] = (
                User(client, data.get("user")) if data.get("user") else None
            )
            self.name: Optional[str] = data.get("name")
            self.avatar: Optional[str] = data.get("avatar")
            self.token: Optional[str] = data.get("token")
            self.application_id: Optional[str] = data.get("application_id")
            self.source_guild: Optional[PartialGuild] = PartialGuild(
                data.get("source_guild")
            )
            self.url: Optional[str] = data.get("url")


class Modal:
    def __init__(self, *, title: str, custom_id: str, components: List[ActionRow]):
        self.title = title
        self.custom_id = custom_id
        self.components = [component.to_dict() for component in components]

    def to_dict(self):
        return {
            "title": self.title,
            "custom_id": self.custom_id,
            "components": self.components,
        }


class BaseInteraction:
    def __init__(self, client, data: dict):
        self.id: str = data.get("id")
        self.client = client
        self.type: int = data.get("type")
        self.application_id: int = data.get("application_id")
        self.data: dict = data
        self.interaction_data: Optional[dict] = data.get("data")
        self.guild_id: Optional[str] = data.get("guild_id")
        self.channel_id: Optional[str] = data.get("channel_id")
        self.author: Optional[Union[User, GuildMember]] = (
            GuildMember(client, data.get("member"))
            if data.get("member")
            else User(client, data.get("user"))
            if data.get("user")
            else None
        )
        self.token: str = data.get("token")
        self.version: int = data.get("version")
        self.locale: Optional[str] = data.get("locale")
        self.guild_locale: Optional[str] = data.get("guild_locale")
        self.original_response: Optional[
            Message
        ] = None  # Can't be set on construction.
        self.followup_response: Optional[
            Message
        ] = None  # Can't be set on construction.

    async def reply(
        self,
        *,
        tts: bool = False,
        content: Optional[str] = None,
        embeds: Optional[List[Embed]] = None,
        allowed_mentions=None,
        components: Optional[List[ActionRow]] = None,
        attachments: Optional[List[Attachment]] = None,
        suppress_embeds: Optional[bool] = False,
        ephemeral: Optional[bool] = False,
    ) -> None:

        message_data = {"tts": tts, "flags": 0}

        if suppress_embeds:
            message_data["flags"] | +1 << 2
        if ephemeral:
            message_data["flags"] |= 1 << 6

        if content:
            message_data["content"] = content
        if embeds:
            message_data["embeds"] = [embed.to_dict() for embed in embeds]
        if allowed_mentions:
            message_data["allowed_mentions"] = allowed_mentions.to_dict()
        if components:
            message_data["components"] = [
                component.to_dict() for component in components
            ]
        if attachments:
            message_data["attachments"] = [
                attachment.to_dict() for attachment in attachments
            ]

        payload = {"type": 4, "data": message_data}
        await self.client.http.post(
            f"/interactions/{self.id}/{self.token}/callback", json=payload
        )

    async def defer(self, *, show_loading_state: Optional[bool] = True):
        if show_loading_state:
            return await self.client.http.post(
                f"/interaction/{self.id}/{self.token}/callback", json={"type": 5}
            )
        else:
            return await self.client.http.post(
                f"/interaction/{self.id}/{self.token}/callback", json={"type": 6}
            )

    async def send_modal(self, modal: Modal):
        if not isinstance(modal, Modal):
            raise InvalidArgumentType("The modal argument must be of type Modal.")
        payload = {"type": 9, "data": modal.to_dict()}
        await self.client.http.post(
            f"/interactions/{self.id}/{self.token}/callback", json=payload
        )

    @property
    def is_ping(self):
        return self.type == 1

    @property
    def is_application_command(self):
        return self.type == 2

    @property
    def is_message_component(self):
        return self.type == 3

    @property
    def is_autocomplete(self):
        return self.type == 4

    @property
    def is_modal_submit(self):
        return self.type == 5

    async def fetch_original_response(self, *, skip_cache: Optional[bool] = False):
        if not skip_cache and self.original_response:
            return self.original_response
        message_data = await self.client.http.get(
            f"/webhooks/{self.application_id}/{self.token}/messages/@original"
        )
        self.original_response = Message(self.client, message_data)
        return self.original_response

    async def edit_original_response(
        self,
        *,
        tts: bool = False,
        content: Optional[str] = None,
        embeds: Optional[List[Embed]] = None,
        allowed_mentions=None,
        components: Optional[List[Union[Button, SelectMenu, TextInput]]] = None,
        attachments: Optional[List[Attachment]] = None,
        suppress_embeds: Optional[bool] = False,
        ephemeral: Optional[bool] = False,
    ) -> None:

        message_data = {"tts": tts, "flags": 0}

        if suppress_embeds:
            message_data["flags"] += 1 << 2
        if ephemeral:
            message_data["flags"] += 1 << 6

        if content:
            message_data["content"] = content
        if embeds:
            message_data["embeds"] = [embed.to_dict() for embed in embeds]
        if allowed_mentions:
            message_data["allowed_mentions"] = allowed_mentions.to_dict()
        if components:
            message_data["components"] = [
                component.to_dict() for component in components
            ]
        if attachments:
            message_data["attachments"] = [
                attachment.to_dict() for attachment in attachments
            ]

        new_message_data = await self.client.http.patch(
            f"/webhooks/{self.application_id}/{self.token}/messages/@original",
            json=message_data,
        )
        self.original_response = Message(self.client, new_message_data)
        return self.original_response

    async def delete_original_response(self):
        await self.client.http.delete(
            f"/webhooks/{self.application_id}/{self.token}/messages/@original"
        )

    async def create_followup(
        self,
        *,
        tts: bool = False,
        content: Optional[str] = None,
        embeds: Optional[List[Embed]] = None,
        allowed_mentions=None,
        components: Optional[List[Union[Button, SelectMenu, TextInput]]] = None,
        attachments: Optional[List[Attachment]] = None,
        suppress_embeds: Optional[bool] = False,
        ephemeral: Optional[bool] = False,
    ) -> None:

        message_data = {"tts": tts, "flags": 0}

        if suppress_embeds:
            message_data["flags"] += 1 << 2
        if ephemeral:
            message_data["flags"] += 1 << 6

        if content:
            message_data["content"] = content
        if embeds:
            message_data["embeds"] = [embed.to_dict() for embed in embeds]
        if allowed_mentions:
            message_data["allowed_mentions"] = allowed_mentions.to_dict()
        if components:
            message_data["components"] = [
                component.to_dict() for component in components
            ]
        if attachments:
            message_data["attachments"] = [
                attachment.to_dict() for attachment in attachments
            ]

        response = await self.client.http.post(
            f"/webhooks/{self.application_id}/{self.token}", json=message_data
        )
        new_message_data = await response.json()
        self.followup_response = Message(self.client, new_message_data)
        return self.followup_response

    async def edit_followup(
        self,
        *,
        tts: bool = False,
        content: Optional[str] = None,
        embeds: Optional[List[Embed]] = None,
        allowed_mentions=None,
        components: Optional[List[Union[Button, SelectMenu, TextInput]]] = None,
        attachments: Optional[List[Attachment]] = None,
        suppress_embeds: Optional[bool] = False,
        ephemeral: Optional[bool] = False,
    ) -> None:

        message_data = {"tts": tts, "flags": 0}

        if suppress_embeds:
            message_data["flags"] += 1 << 2
        if ephemeral:
            message_data["flags"] += 1 << 6

        if content:
            message_data["content"] = content
        if embeds:
            message_data["embeds"] = [embed.to_dict() for embed in embeds]
        if allowed_mentions:
            message_data["allowed_mentions"] = allowed_mentions.to_dict()
        if components:
            message_data["components"] = [
                component.to_dict() for component in components
            ]
        if attachments:
            message_data["attachments"] = [
                attachment.to_dict() for attachment in attachments
            ]

        await self.client.http.patch(
            f"/webhook/{self.application_id}/{self.token}/", json=message_data
        )

    async def delete_followup(self):
        return await self.client.http.delete(
            f"/webhook/{self.application_id}/{self.token}/"
        )


class MessageComponentInteraction(BaseInteraction):
    def __init__(self, client, data: dict):
        super().__init__(client, data)
        self.message: Message = Message(client, data.get("message"))
        self.custom_id: str = self.interaction_data.get("custom_id")
        self.component_type: Optional[int] = self.interaction_data.get("component_type")
        self.values: Optional[dict] = [
            SelectMenuOption(option)
            for option in self.interaction_data.get("values", [])
        ]

    def is_action_row(self):
        return self.component_type == 1

    def is_button(self):
        return self.component_type == 2

    def is_select_menu(self):
        return self.component_type == 3

    def is_text_input(self):
        return self.component_type == 4

    async def update(
        self,
        *,
        tts: bool = False,
        content: Optional[str] = None,
        embeds: Optional[List[Embed]] = None,
        allowed_mentions=None,
        components: Optional[List[Union[Button, SelectMenu, TextInput]]] = None,
        attachments: Optional[List[Attachment]] = None,
        suppress_embeds: Optional[bool] = False,
    ) -> None:

        message_data = {"tts": tts, "flags": 0}

        if suppress_embeds:
            message_data["flags"] += 1 << 2

        if content:
            message_data["content"] = content
        if embeds:
            message_data["embeds"] = [embed.to_dict() for embed in embeds]
        if allowed_mentions:
            message_data["allowed_mentions"] = allowed_mentions.to_dict()
        if components:
            message_data["components"] = [
                component.to_dict() for component in components
            ]
        if attachments:
            message_data["attachments"] = [
                attachment.to_dict() for attachment in attachments
            ]

        payload = {"type": 7, "data": message_data}

        await self.client.http.patch(
            f"/interaction/{self.id}/{self.token}/callback", json=payload
        )

    async def defer_update(self):
        await self.client.http.post(
            f"/interaction/{self.id}/{self.token}/callback", json={"type": 6}
        )


class ModalSubmitInteraction(BaseInteraction):
    def __init__(self, client, data: dict):
        super().__init__(client, data)
        self.custom_id: str = self.interaction_data["custom_id"]
        self._components: List[
            Union[Button, SelectMenu, TextInput]
        ] = self.interaction_data.get("components")

    async def send_modal(self, *args, **kwargs):
        raise NotImplementedError("ModalSubmitInteractions cannot send modals.")


class ApplicationCommandOption:
    def __init__(self, data: dict):
        self.command_name: str = data.get("name")
        self.command_type: int = data.get("type")
        self.value: Optional[Union[str, int, float]] = data.get("value")
        self.focused: Optional[bool] = data.get("focused")


class AutoCompleteInteraction(BaseInteraction):
    def __init__(self, client, data: dict):
        super().__init__(client, data)
        self.options: List[ApplicationCommandOption] = [
            ApplicationCommandOption(option) for option in data.get("options", [])
        ]

    async def reply(self, choices: List[SlashCommandOptionChoice]) -> None:
        payload = {"type": 9, "data": []}

        for choice in choices:
            if not isinstance(choice, SlashCommandOptionChoice):
                raise TypeError(f"{choice} must be of type SlashCommandOptionChoice")
            payload["data"]["choices"].append(choice.to_dict())

        await self.client.http.post(
            f"/interactions/{self.id}/{self.token}/callback", json=payload
        )


class ApplicationCommandSubcommandOption(ApplicationCommandOption):
    def __init__(self, data: dict):
        super().__init__(data)
        self.options: List[ApplicationCommandOption] = [
            ApplicationCommandOption(option) for option in data.get("options", [])
        ]


class ResolvedDataHandler:
    def __init__(self, client, resolved_data: dict):
        self.data: dict = resolved_data
        ...


class ApplicationCommandInteraction(BaseInteraction):
    def __init__(self, client, data: dict):
        super().__init__(client, data)
        self.command_id: str = self.interaction_data.get("id")
        self.command_name: str = self.interaction_data.get("name")
        self.command_type: int = self.interaction_data.get("type")
        self.resolved: ResolvedDataHandler(client, data.get("resolved", {}))
        self.options: List[dict] | None = self.interaction_data.get("options", [])


class UserCommandInteraction(ApplicationCommandInteraction):
    def __init__(self, client, data: dict):
        super().__init__(client, data)
        self.target_id: str = data.get("target_id")


class MessageCommandInteraction(UserCommandInteraction):
    ...  # Literally the same thing.


class Invite:
    def __init__(self, data: dict):
        self.code: str = data.get("code")
        self.guild: Optional[PartialGuild] = (
            PartialGuild(data.get("guild")) if data.get("guild") else None
        )
        self.channel: GuildChannel = (
            GuildChannel(data.get("channel")) if data.get("channel") else None
        )
        self.inviter: Optional[User] = (
            User(data.get("inviter")) if data.get("inviter") else None
        )
        self.target_type: int = data.get("target_type")
        self.target_user: Optional[User] = (
            User(data.get("target_user")) if data.get("target_user") else None
        )
        self.target_application: Optional[Application] = (
            Application(data.get("target_application"))
            if data.get("target_application")
            else None
        )
        self.approximate_presence_count: Optional[int] = data.get(
            "approximate_presence_count"
        )
        self.approximate_member_count: Optional[int] = data.get(
            "approximate_member_count"
        )
        self.expires_at: Optional[str] = data.get("expires_at")
        self.stage_instance: Optional[GuildStageChannel] = (
            GuildStageChannel(data.get("stage_instance"))
            if data.get("stage_instance")
            else None
        )
        self.guild_scheduled_event: Optional[GuildScheduledEvent] = GuildScheduledEvent(
            data.get("guild_scheduled_event")
        )


class GuildMember(User):
    def __init__(self, client, data: dict):
        super().__init__(client, data.get("user"))
        self.data = data
        self.client = client
        self.nick: Optional[str] = data.get("nick")
        self.avatar: Optional[str] = data.get("avatar")
        self.role_ids: Optional[List[str]] = list(data.get("roles", []))
        self.joined_at: str = data.get("joined_at")
        self.premium_since: Optional[str] = data.get("premium_since")
        self.deaf: bool = data.get("deaf")
        self.mute: bool = data.get("mute")
        self.pending: Optional[bool] = data.get("pending")
        self.permissions: Optional[str] = data.get("permissions")
        self.communication_disabled_until: Optional[str] = data.get(
            "communication_disabled_until"
        )


class MentionedChannel:
    def __init__(self, data: dict):
        self.id: str = data.get("id")
        self.guild_id: str = data.get("guild_id")
        self.type: int = data.get("type")
        self.name: str = data.get("name")


class MentionedUser(User):
    def __init__(self, client, data: dict):
        super().__init__(client, data)
        self.member: Optional[GuildMember] = (
            GuildMember(client, data.get("member")) if data.get("member") else None
        )


class MessageActivity:
    def __init__(self, data: dict):
        self.type: int = data.get("type")
        self.party_id: Optional[str] = data.get("party_id")


class AllowedMention:
    def __init__(
        self,
        allowed_mentions: List[str],
        replied_user: bool,
        roles: List[str],
        users: List[str],
    ):
        self.data = {
            "parse": allowed_mentions,
            "replied_user": replied_user,
            "roles": roles,
            "users": users,
        }


class MessageInteraction:
    def __init__(self, client, data: dict):
        self.id: str = data.get("id")
        self.type: int = data.get("type")
        self.name: str = data.get("name")
        self.user: User = User(client, data.get("user"))
        payload = {}
        if data.get("user"):
            payload.update(data.get("user"))
        if data.get("member"):
            payload.update(data.get("member"))
        if data.get("user") and not data.get("member"):
            payload = {**data.get("user")}

        self.member: Optional[GuildMember] = (
            GuildMember(client, payload) if data.get("member") else None
        )
        self.user = User(client, data.get("user"))


class SlashCommand(ApplicationCommand):
    def __init__(self, data: dict):
        super().__init__(data)
        self.options: Optional[List[AnyOption]] = data.get(
            "options"
        )  # Return the type hinted class later this will take too long and
        # is very tedious, I'll probably get Copilot to do it for me lmao
        for option in self.options:
            option_type = option.get("type")
            if option_type == 1:
                return Subcommand(option)
            elif option_type == 2:
                return SubCommandGroup(option)
            elif option_type == 3:
                return StringOption(option)
            elif option_type == 4:
                return IntegerOption(option)
            elif option_type == 5:
                return BooleanOption(option)
            elif option_type == 6:
                return UserOption(option)
            elif option_type == 7:
                return ChannelOption(option)
            elif option_type == 8:
                return RoleOption(option)
            elif option_type == 9:
                return MentionableOption(option)
            elif option_type == 10:
                return NumberOption(option)
            elif option_type == 11:
                return AttachmentOption(option)

    def to_dict(self):
        json_options = [option.to_dict for option in self.options]
        return {
            "name": self.name,
            "type": self.type,
            "description": self.description,
            "options": json_options,
        }


class TeamMember:
    def __init__(self, data: dict):
        self.data = data
        self.membership_state: int = data.get("membership_state")
        self.team_id: str = data.get("team_id")
        self.user: PartialUser = PartialUser(data.get("user"))


class Team:
    def __init__(self, data: dict):
        self.data = data
        self.icon: str = data.get("icon")
        self.id: str = data.get("id")
        self.members: List[TeamMember] = data.get("members")


class ClientUser:
    def __init__(self, client, data: dict):
        self.client = client
        self.data = data
        self.verified: bool = data.get("verified")
        self.username: str = data.get("username")
        self.mfa_enabled: bool = data.get("mfa_enabled")
        self.id: str = data.get("id")
        self.flags: int = data.get("flags")
        self.email: Optional[str] = data.get("email")
        self.discriminator: str = data.get("discriminator")
        self.bot: bool = data.get("bot")
        self.avatar: str = data.get("avatar")
        if not self.bot:  # if they're a user account
            logger.warning(
                "Warning: Self botting is against Discord ToS." " You can get banned. "
            )

    async def fetch(self):
        response = await self.client.http.get("users/@me")
        data = await response.json()
        super().__init__(data)  # Reinitialize the class with the new data.

    async def edit(
        self, *, username: Optional[str] = None, avatar: Optional[bytes] = None
    ):
        payload = {}
        if username:
            payload["username"] = username
        if avatar:
            payload["avatar"] = self.client.utils.bytes_to_base64_data(avatar)
        response = await self.client.http.patch("users/@me", json=payload)
        data = await response.json()
        # Reinitialize the class with the new data, the full data.
        self.__init__(data)


class SourceChannel:
    def __init__(self, data: dict):
        self.id: str = data.get("id")
        self.name: str = data.get("name")


class Webhook:  # Not used for making webhooks.
    def __init__(self, client, data: dict):
        self.id: str = data.get("id")
        self.client = client
        self.type: int = (
            "Incoming"
            if data.get("type") == 1
            else "Channel Follower"
            if data.get("type") == 2
            else "Application"
        )
        self.guild_id: Optional[str] = data.get("guild_id")
        self.channel_id: Optional[str] = data.get("channel_id")
        self.user: Optional[WebhookUser] = (
            WebhookUser(data.get("user")) if data.get("user") else None
        )
        self.name: Optional[str] = data.get("name")
        self.avatar: Optional[str] = data.get("avatar")
        self.token: str = data.get("token")
        self.application_id: Optional[str] = data.get("application_id")
        self.source_guild: Optional[PartialGuild] = PartialGuild(
            data.get("source_guild")
        )
        self.source_channel: Optional[SourceChannel] = SourceChannel(
            data.get("source_channel")
        )
        self.url: Optional[str] = data.get("url")


class Flag:
    if TYPE_CHECKING:
        class_flags: "dict[str, Any]"

    def __init_subclass__(cls) -> None:
        cls.class_flags = {k: v for k, v in cls.__dict__.items() if isinstance(v, int)}
        return cls

    def __init__(self, value: int = 0, **kwargs):
        self.value = value
        self.turned_on: "list[str]" = [k for k, a in kwargs.items() if a]

        for k, v in self.class_flags.items():
            if v & value and k not in self.turned_on:
                self.turned_on.append(k)

        self.calculate_from_turned()

    def calculate_from_turned(self):
        value = 0
        for key, flag in self.class_flags.items():
            if key in self.class_flags:
                value |= flag
        self.value = value

    def __getattribute__(self, __name: str) -> Any:
        original = super().__getattribute__
        if __name in original("class_flags"):
            return __name in original("turned_on")
        return original(__name)

    def __setattr__(self, __name: str, __value: Any) -> None:
        if __name not in self.class_flags:
            return super().__setattr__(__name, __value)
        if __value and __name not in self.turned_on:
            self.turned_on.append(__name)
        elif not __value and __name in self.turned_on:
            self.turned_on.remove(__name)
        self.calculate_from_turned()

    @classmethod
    def all(cls):
        return cls(**{k: True for k in cls.class_flags})


class Intents(Flag):
    guilds = 1 << 0
    members = 1 << 1
    bans = 1 << 2
    emojis_and_stickers = 1 << 3
    integrations = 1 << 4
    webhooks = 1 << 5
    invites = 1 << 6
    voice_states = 1 << 7
    presences = 1 << 8

    guild_messages = 1 << 9
    guild_message_reactions = 1 << 10
    guild_message_typing = 1 << 11

    direct_messages = 1 << 12
    direct_message_reactions = 1 << 13
    direct_message_typing = 1 << 14

    message_content = 1 << 15
    scheduled_event = 1 << 16


class Permissions(Flag):
    create_instant_invite = 1 << 0
    kick_members = 1 << 1
    ban_members = 1 << 2
    administrator = 1 << 3
    manage_channels = 1 << 4
    manage_guild = 1 << 5
    add_reactions = 1 << 6
    view_audit_log = 1 << 7
    priority_speaker = 1 << 8
    stream = 1 << 9
    read_messages = 1 << 10
    send_messages = 1 << 11
    send_tts_messages = 1 << 12
    manage_messages = 1 << 13
    embed_links = 1 << 14
    attach_files = 1 << 15
    read_message_history = 1 << 16
    mention_everyone = 1 << 17
    use_external_emojis = 1 << 18
    connect = 1 << 20
    speak = 1 << 21
    mute_members = 1 << 22
    deafen_members = 1 << 23
    move_members = 1 << 24
    use_voice_activation = 1 << 25
    change_nickname = 1 << 26
    manage_nicknames = 1 << 27
    manage_roles = 1 << 28
    manage_webhooks = 1 << 29
    manage_emojis_and_stickers = 1 << 30
    use_application_commands = 1 << 31
    request_to_speak = 1 << 32
    manage_events = 1 << 33
    manage_threads = 1 << 34
    create_public_threads = 1 << 35
    create_private_threads = 1 << 36
    use_external_stickers = 1 << 37
    send_messages_in_threads = 1 << 38
    start_embedded_activities = 1 << 39
    moderator_members = 1 << 40


class VoiceState:
    def __init__(self, client, data: dict):
        self.data: dict = data
        self.guild_id: Optional[str] = data.get("guild_id")
        self.channel_id: str = data.get("channel_id")
        self.user_id: str = data.get("user_id")
        self.member: Optional[GuildMember] = (
            GuildMember(client, data.get("member")) if data.get("member") else None
        )
        self.session_id: str = data.get("session_id")
        self.deaf: bool = data.get("deaf")
        self.mute: bool = data.get("mute")
        self.self_deaf: bool = data.get("self_deaf")
        self.self_mute: bool = data.get("self_mute")
        self.self_stream: Optional[bool] = data.get("self_stream")
        self.self_video: bool = data.get("self_video")
        self.suppress: bool = data.get("suppress")
        self.request_to_speak_timestamp: Optional[datetime.datetime] = (
            datetime.datetime.fromisoformat(data.get("request_to_speak_timestamp"))
            if data.get("request_to_speak_timestamp")
            else None
        )


class Paginator:
    def __init__(self, *, pages: List[Embed]):
        self.current_index: int = 0
        self.__pages = pages

    def __iter__(self):
        return self

    def __len__(self):
        return len(self.__pages)

    def __next__(self):
        return self.forward()

    @property
    def page(self):
        return self.__pages[self.current_index]

    def forward(self):
        self.current_index = min(len(self.__pages), self.current_index + 1)
        return self.__pages[self.current_index]

    def back(self):
        self.current_index = max(0, self.current_index - 1)
        return self.__pages[self.current_index]

    def first(self):
        self.current_index = 0

    def last(self):
        self.current_index = len(self.__pages)

    def add_page(self, page: Embed):
        self.__pages.append(page)

    def insert_page(self, page: Embed, index: int):
        if index >= len(self.__pages):
            self.add_page(page)
            return

        self.__pages.index(page, index)

    def remove_page(self, page: Embed):
        self.__pages = list(filter(lambda embed: embed != page, self.__pages))


class Connectable:
    def __init__(
        self,
        client,
        *,
        guild_id: Optional[str] = None,
        channel_id: Optional[str] = None,
        channel: Optional[VoiceChannel] = None,
    ):
        self.client = client
        # TODO: Figure out which one I will use later in production
        if channel:
            self.guild_id = channel.guild.id
            self.channel_id = channel.id
        else:
            self.guild_id = guild_id
            self.channel_id = channel_id

        self._closed = True

        self.token: Optional[str] = None
        self.session_id: Optional[str] = None
        self.endpoint: Optional[str] = None
        self.socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setblocking(False)
        self.ws: Optional[ClientWebSocketResponse] = None

        self.heartbeat_interval: Optional[int] = None
        self.server_ip: Optional[str] = None
        self.server_port: Optional[int] = None
        self.ssrc: Optional[int] = None
        self.mode: Optional[List[str]] = None
        self.secret_key: Optional[str] = None

        self.ip: Optional[str] = None
        self.port: Optional[int] = None

    async def connect(
        self, muted: Optional[bool] = False, deafened: Optional[bool] = False
    ):
        await self.client.send_json(
            {
                "op": GatewayOpcode.VOICE_STATE_UPDATE,
                "d": {
                    "guild_id": self.guild_id,
                    "channel_id": self.channel_id,
                    "self_mute": muted,
                    "self_deaf": deafened,
                },
            }
        )
        voice_state_update_coro = asyncio.create_task(
            self.client.wait_for("voice_state_update")
        )
        if not self.client.intents.voice_states:
            raise ValueError(
                "You must have the `voice_states` intent enabled to use "
                "this otherwise we never get the session_id."
            )

        voice_server_update_coro = asyncio.create_task(
            self.client.wait_for(
                "voice_server_update", check=lambda data: data.get("endpoint")
            )
        )
        events, _ = await asyncio.wait(
            [voice_state_update_coro, voice_server_update_coro]
        )
        for event in events:
            if isinstance(event.result(), VoiceState):  # If it's the VoiceState
                self.session_id = event.result().session_id
            elif isinstance(event.result(), dict):  # If it's a VoiceServerUpdate
                self.token = event.result()["token"]
                self.endpoint = event.result()["endpoint"]

        await self._connect_ws()

    async def _connect_ws(self):
        wss = "" if self.endpoint.startswith("wss://") else "wss://"
        self.ws = await self.client.http.ws_connect(f"{wss}{self.endpoint}?v=4")
        return await self.handle_events()

    async def handle_events(self):
        async for event in self.ws:
            event = event.json()
            if event["op"] == VoiceOpcode.HELLO:
                await self.handle_hello(event["d"])

            elif event["op"] == VoiceOpcode.READY:
                await self.handle_ready(event["d"])

        await self.handle_close()

    async def handle_close(self):
        self._closed = True
        if self.ws.close_close == GatewayCECode.UnknownOpcode:
            raise ClosedWebSocketConnection(
                "EpikCord has sent an invalid OpCode to the Voice WebSocket. Report this at https://github.com/EpikCord/EpikCord.py/issues"
            )
        elif self.ws.close_code == GatewayCECode.DecodeError:
            raise ClosedWebSocketConnection(
                "EpikCord has sent an invalid identify to the Voice WebSocket. Report this at https://github.com/EpikCord/EpikCord.py/issues"
            )
        elif self.ws.close_code == GatewayCECode.NotAuthenticated:
            raise ClosedWebSocketConnection(
                "EpikCord has sent a payload before identifying to the Voice Websocket. Report this at https://github.com/EpikCord/EpikCord.py/issues"
            )
        elif self.ws.close_code == GatewayCECode.AuthenticationFailed:
            raise ClosedWebSocketConnection(
                "EpikCord sent an invalid token to the Voice Websocket. Report this at https://github.com/EpikCord/EpikCord.py/issues"
            )
        elif self.ws.close_code == GatewayCECode.AlreadyAuthenticated:
            raise ClosedWebSocketConnection(
                "EpikCord sent more than one identify payload. Report this at https://github.com/EpikCord/EpikCord.py/issues"
            )
        elif self.ws.close_code == GatewayCECode.SessionTimedOut:

            raise ClosedWebSocketConnection("The session is no longer valid.")

    async def handle_hello(self, data: dict):
        self.heartbeat_interval = data["heartbeat_interval"]
        await self.identify()

        async def wrapper():
            while True:
                await self.heartbeat()
                await asyncio.sleep(self.heartbeat_interval / 1000)

        loop = asyncio.get_event_loop()
        loop.create_task(wrapper())

    async def handle_ready(self, event: dict):
        self.ssrc: int = event["ssrc"]
        self.mode = event["modes"][0]  # Always has one mode, and I can use any.
        self.server_ip: str = event["ip"]
        self.server_port: int = event["port"]

    async def handle_session_description(self, event: dict):
        self.secret_key: str = event["d"]["secret_key"]

    async def identify(self):
        return await self.send_json(
            {
                "op": VoiceOpcode.IDENTIFY,
                "d": {
                    "server_id": self.guild_id,
                    "user_id": self.client.user.id,
                    "session_id": self.session_id,
                    "token": self.token,
                },
            }
        )

    async def select_protocol(self):
        await self.send_json(
            {
                "op": VoiceOpcode.SELECT_PROTOCOL,
                "d": {
                    "protocol": "udp",  # I don't understand UDP tbh
                    "data": {"address": self.ip, "port": self.port, "mode": self.mode},
                },
            }
        )

    async def send_json(self, json, *args, **kwargs):
        await self.ws.send_json(json, *args, **kwargs)
        logger.info(f"Sent {json} to Voice Websocket {self.endpoint}")

    async def heartbeat(self):
        heartbeat_nonce = nacl.utils.random(nacl.secret.SecretBox.NONCE_SIZE)
        return await self.send_json({"op": VoiceOpcode.HEARTBEAT, "d": heartbeat_nonce})

    async def discover_ip(self):
        udp_packet: bytearray = bytearray(70)
        struct.pack_into(">H", udp_packet, 0, 1)  # Request. At the 0th Index, write 0x1
        struct.pack_into(">H", udp_packet, 2, 70)  # Length of the packet.
        struct.pack_into(">I", udp_packet, 4, self.ssrc)
        self.socket.sendto(udp_packet, (self.server_ip, self.server_port))
        ip_data = await asyncio.get_event_loop().sock_recv(self.socket, 70)
        # type + length = 4
        # We need to start at index 4 to get the address and ignore the type and length
        ip_end = ip_data.index(0, 4)
        self.ip = ip_data[4:ip_end].decode("ascii")
        self.port = struct.unpack_from(">H", ip_data, len(ip_data) - 2)[0]


class VoiceChannel(GuildChannel, Messageable, Connectable):
    def __init__(self, client, data: dict):
        super().__init__(client, data)
        self.bitrate: int = data.get("bitrate")
        self.user_limit: int = data.get("user_limit")
        self.rtc_region: str = data.get("rtc_region")


class Utils:
    """
    A utility class, used to make difficult things easy.

    Attributes:
    -----------
    client: Client
        The client that this utility class is attached to.

    """

    channels_types = {
        0: GuildTextChannel,
        1: DMChannel,
        2: VoiceChannel,
        4: ChannelCategory,
        5: GuildNewsChannel,
        10: GuildNewsThread,
        11: Thread,
        12: PrivateThread,
        13: GuildStageChannel,
    }

    component_types = {2: Button, 3: SelectMenu, 4: TextInput}

    interaction_types = {
        2: ApplicationCommandInteraction,
        3: MessageComponentInteraction,
        4: AutoCompleteInteraction,
        5: ModalSubmitInteraction,
    }

    def __init__(self, client):
        self.client = client
        self._MARKDOWN_ESCAPE_SUBREGEX = "|".join(
            r"\{0}(?=([\s\S]*((?<!\{0})\{0})))".format(c)
            for c in ("*", "`", "_", "~", "|")
        )

        self._MARKDOWN_ESCAPE_COMMON = r"^>(?:>>)?\s|\[.+\]\(.+\)"

        self._MARKDOWN_ESCAPE_REGEX = re.compile(
            rf"(?P<markdown>{self._MARKDOWN_ESCAPE_SUBREGEX}|{self._MARKDOWN_ESCAPE_COMMON})",
            re.MULTILINE,
        )

        self._URL_REGEX = (
            r"(?P<url><[^: >]+:\/[^ >]+>|(?:https?|steam):\/\/[^\s<]+[^<.,:;\"\'\]\s])"
        )

        self._MARKDOWN_STOCK_REGEX = (
            rf"(?P<markdown>[_\\~|\*`]|{self._MARKDOWN_ESCAPE_COMMON})"
        )

    @staticmethod
    def get_mime_type_for_image(data: bytes):
        if data.startswith(b"\x89\x50\x4E\x47\x0D\x0A\x1A\x0A"):
            return "image/png"
        elif data[:3] == b"\xff\xd8\xff" or data[6:10] in (b"JFIF", b"Exif"):
            return "image/jpeg"
        elif data.startswith(
            (b"\x47\x49\x46\x38\x37\x61", b"\x47\x49\x46\x38\x39\x61")
        ):
            return "image/gif"
        elif data.startswith(b"RIFF") and data[8:12] == b"WEBP":
            return "image/webp"
        else:
            raise InvalidArgumentType("Unsupported image type given")

    def _bytes_to_base64_data(self, data: bytes) -> str:
        fmt = "data:{mime};base64,{data}"
        mime = self.get_mime_type_for_image(data)
        b64 = b64encode(data).decode("ascii")
        return fmt.format(mime=mime, data=b64)

    def component_from_type(self, component_data: dict):
        component_type = component_data.get("type")
        component_cls = self.component_types.get(component_type)

        if not component_cls:
            logger.warning(f"Unknown component type: {component_type}")
            return

        return component_cls(**component_data)

    def match_mixed(self, variant_one: str, variant_two: str):
        """Matches and returns a single output from two"""
        return (
            variant_one if not variant_two else variant_two if not variant_one else None
        )

    def interaction_from_type(self, data):
        interaction_type = data["type"]
        interaction_cls = self.interaction_types.get(interaction_type)

        if not interaction_cls:
            logger.warning(f"Unknown interaction type: {interaction_type}")
            return

        return interaction_cls(self.client, data)

    def channel_from_type(self, channel_data: dict):
        channel_type = channel_data.get("type")
        channel_cls = self.channels_types.get(channel_type)

        if not channel_cls:
            raise InvalidArgumentType(f"Unknown channel type: {channel_type}")

        return channel_cls(self.client, channel_data)

    @staticmethod
    def compute_timedelta(dt: datetime.datetime):
        if dt.tzinfo is None:
            dt = dt.astimezone()
        now = datetime.datetime.now(datetime.timezone.utc)
        return max((dt - now).total_seconds(), 0)

    async def sleep_until(
        self, when: Union[datetime.datetime, int, float], result: Optional[T] = None
    ) -> Optional[T]:
        if when == datetime.datetime:
            delta = self.compute_timedelta(when)

        return await asyncio.sleep(delta if when == datetime.datetime else when, result)

    def remove_markdown(self, text: str, *, ignore_links: bool = True) -> str:
        def replacement(match):
            groupdict = match.groupdict()
            return groupdict.get("url", "")

        regex = self._MARKDOWN_STOCK_REGEX
        if ignore_links:
            regex = f"(?:{self._URL_REGEX}|{regex})"
        return re.sub(regex, replacement, text, 0, re.MULTILINE)

    def escape_markdown(
        self, text: str, *, as_needed: bool = False, ignore_links: bool = True
    ) -> str:
        if not as_needed:

            def replacement(match):
                groupdict = match.groupdict()
                if is_url := groupdict.get("url"):
                    return is_url
                return "\\" + groupdict["markdown"]

            regex = self._MARKDOWN_STOCK_REGEX
            if ignore_links:
                regex = f"(?:{self._URL_REGEX}|{regex})"
            return re.sub(regex, replacement, text, 0, re.MULTILINE)
        else:
            text = re.sub(r"\\", r"\\\\", text)
            return self._MARKDOWN_ESCAPE_REGEX.sub(r"\\\1", text)

    @staticmethod
    def escape_mentions(text: str) -> str:
        return re.sub(r"@(everyone|here|[!&]?\d{17,20})", "@\u200b\\1", text)

    @staticmethod
    def utcnow() -> datetime.datetime:
        return datetime.datetime.now(datetime.timezone.utc)

    @staticmethod
    def cancel_tasks(loop) -> None:
        tasks = {t for t in asyncio.all_tasks(loop=loop) if not t.done()}

        if not tasks:
            return

        for task in tasks:
            task.cancel()
        logger.debug(f"Cancelled {len(tasks)} tasks")
        loop.run_until_complete(asyncio.gather(*tasks, return_exceptions=True))

    def cleanup_loop(self, loop) -> None:
        try:
            self.cancel_tasks(loop)
            logger.debug("Shutting down async generators.")
            loop.run_until_complete(loop.shutdown_asyncgens())
        finally:
            loop.close()


class Shard(WebsocketClient):
    def __init__(
        self,
        token,
        intents,
        shard_id,
        number_of_shards,
        presence: Optional[Presence] = None,
    ):
        super().__init__(token, intents, presence)
        self.shard_id = [shard_id, number_of_shards]

    async def identify(self):
        payload = {
            "op": GatewayOpcode.IDENTIFY,
            "d": {
                "token": self.token,
                "intents": self.intents.value,
                "properties": {
                    "os": platform,
                    "browser": "EpikCord.py",
                    "device": "EpikCord.py",
                },
                "shard": str(self.shard_id),
            },
        }

        if self.presence:
            payload["d"]["presence"] = self.presence.to_dict()

        await self.send_json(payload)

    async def reconnect(self):
        await self.close()
        await self.connect()
        await self.identify()
        await self.resume()


class ShardManager:
    def __init__(
        self,
        token: str,
        *,
        intents: Optional[Union[Intents, int]],
        shards: Optional[int] = None,
    ):
        self.token: str = token
        self.http: HTTPClient = HTTPClient(
            headers={
                "Authorization": f"Bot {token}",
                "User-Agent": f"DiscordBot (https://github.com/EpikCord/EpikCord.py {__version__})",
            }
        )
        self.intents: Intents = (
            intents if isinstance(intents, Intents) else Intents(intents)
        )
        self.desired_shards: Optional[int] = shards
        self.shards: List[Shard] = []

    def run(self):
        async def wrapper():
            endpoint_data = await self.http.get("/gateway/bot")  # ClientResponse
            endpoint_data = await endpoint_data.json()  # Dict

            max_concurrency = endpoint_data["session_start_limit"]["max_concurrency"]

            shards = self.desired_shards

            if not shards:
                shards = endpoint_data["shards"]

            for shard_id in range(shards):
                self.shards.append(Shard(self.token, self.intents, shard_id, shards))

            current_iteration = 0  # The current shard_id we've run

            for shard in self.shards:
                shard.login()
                current_iteration += 1
                if current_iteration == max_concurrency:
                    await asyncio.sleep(5)
                    current_iteration = 0  # Reset it

        loop = asyncio.get_event_loop()
        loop.run_until_complete(wrapper())


class Check:
    def __init__(self, callback):
        self.callback = callback
        self.success_callback = self.default_success
        self.failure_callback = self.default_failure

    def success(self, callback: Optional[Callable] = None):
        self.success_callback = callback or self.default_success

    def failure(self, callback: Optional[Callable] = None):
        self.failure_callback = callback or self.default_failure

    async def default_success(self, interaction):
        logger.info(
            f"{interaction.author.username} ({interaction.author.id}) passed "
            f"the check {self.command_callback.__name__}. "
        )

    async def default_failure(self, interaction):
        logger.critical(
            f"{interaction.author.username} ({interaction.author.id}) failed "
            f"the check {self.command_callback.__name__}. "
        )
        raise FailedCheck(
            f"{interaction.author.username} ({interaction.author.id}) failed "
            f"the check {self.command_callback.__name__}. "
        )


class CommandUtils:
    @staticmethod
    def check(callback):
        return Check(callback)

    @staticmethod
    def user_command(name: Optional[str] = None):
        def register_user_command(func):
            return ClientUserCommand(name=name or func.__name__, callback=func)

        return register_user_command

    @staticmethod
    def message_command(name: Optional[str] = None):
        def register_message_command(func):
            return ClientMessageCommand(name=name or func.__name__, callback=func)

        return register_message_command

    @staticmethod
    def command(
        *,
        name: Optional[str] = None,
        description: str = None,
        guild_ids: Optional[List[str]] = None,
        options: Optional[List[AnyOption]] = None,
    ):
        def register_slash_command(func):
            desc = description or func.__doc__
            if not desc:
                raise TypeError(
                    f"Command with {name or func.__name__} has no description. This is required."
                )
            return ClientSlashCommand(
                name=name or func.__name__,
                description=desc,
                guild_ids=guild_ids or [],
                options=options or [],
            )

        return register_slash_command

    @staticmethod
    def event(name: Optional[str] = None):
        def register_event(func):
            return Event(callback=func, event_name=name or func.__name__)

        return register_event


class AutoModerationTriggerMetaData:
    def __init__(self, data: dict):
        self.keyword_filter: List[str] = data.get("keyword_filter")
        self.presets: List[AutoModerationKeywordPresetTypes] = [
            AutoModerationKeywordPresetTypes(x) for x in data.get("presets")
        ]

    def to_dict(self):
        return {
            "keyword_filter": self.keyword_filter,
            "presets": [int(preset) for preset in self.presets],
        }


class AutoModerationActionMetaData:
    def __init__(self, data: dict):
        self.channel_id: str = data.get("channel_id")
        self.duration_seconds: int = data.get("duration_seconds")

    def to_dict(self):
        return {
            "channel_id": self.channel_id,
            "duration_seconds": self.duration_seconds,
        }


class AutoModerationAction:
    def __init__(self, data: dict):
        self.type: int = AutoModerationActionType(data["type"])
        self.metadata: AutoModerationActionMetaData = AutoModerationActionMetaData(
            data["metadata"]
        )

    def to_dict(self):
        return {
            "type": int(self.type),
            "metadata": self.metadata.to_dict(),
        }


class AutoModerationRule:
    def __init__(self, client, data: dict):
        self.client = client
        self.id: str = data["id"]
        self.guild_id: str = data["guild_id"]
        self.name: str = data["name"]
        self.creator_id: str = data["creator_id"]
        self.event_type: AutoModerationEventType = AutoModerationEventType(
            data["event_type"]
        )
        self.trigger_type: AutoModerationTriggerType = AutoModerationTriggerType(
            data["trigger_type"]
        )
        self.trigger_metadata: AutoModerationTriggerMetaData = [
            AutoModerationTriggerMetaData(data) for data in data["trigger_metadata"]
        ]
        self.actions: List[AutoModerationAction] = [
            AutoModerationAction(data) for data in data.get("actions")
        ]
        self.enabled: bool = data["enabled"]
        self.except_roles_ids: List[str] = data["except_roles"]
        self.except_channels_ids: List[str] = data["except_channels"]

    async def edit(
        self,
        *,
        name: Optional[str] = None,
        event_type: Optional[int] = None,
        trigger_metadata: Optional[AutoModerationTriggerMetaData] = None,
        actions: Optional[List[AutoModerationAction]] = None,
        enabled: Optional[bool] = None,
        exempt_roles: Optional[List[str]] = None,
        exempt_channels: Optional[List[str]] = None,
    ):
        payload = {}

        if name:
            payload["name"] = name

        if event_type:
            payload["event_type"] = int(event_type)

        if enabled is not None:
            payload["enabled"] = enabled

        if exempt_channels:
            payload["exempt_channels"] = exempt_channels

        if exempt_roles:
            payload["exempt_roles"] = exempt_roles

        if trigger_metadata is not None:
            payload["trigger_metadata"] = trigger_metadata.to_dict()

        if actions:
            payload["actions"] = [action.to_dict() for action in actions]

        await self.client.http.patch(
            f"/guilds/{self.guild_id}/auto-moderation/rules/{self.id}", json=payload
        )

    async def delete(self):
        await self.client.http.delete(
            f"guilds/{self.guild_id}/auto-moderation/rules/{self.id}"
        )
        return


__slots__ = __all__ = (
    "ActionRow",
    "Activity",
    "AllowedMention",
    "AnyChannel",
    "AnyOption",
    "Application",
    "ApplicationCommand",
    "ApplicationCommandInteraction",
    "ApplicationCommandOption",
    "ApplicationCommandPermission",
    "ApplicationCommandSubcommandOption",
    "Attachment",
    "AttachmentOption",
    "AutoCompleteInteraction",
    "AutoModerationAction",
    "AutoModerationActionMetaData",
    "AutoModerationActionType",
    "AutoModerationEventType",
    "AutoModerationKeywordPresetTypes",
    "AutoModerationRule",
    "AutoModerationTriggerMetaData",
    "AutoModerationTriggerType",
    "BaseChannel",
    "BaseCommand",
    "BaseComponent",
    "BaseInteraction",
    "BaseSlashCommandOption",
    "BooleanOption",
    "Bucket",
    "Button",
    "ButtonStyle",
    "CacheManager",
    "ChannelCategory",
    "ChannelManager",
    "ChannelOption",
    "ChannelTypes",
    "Check",
    "Client",
    "ClientApplication",
    "ClientMessageCommand",
    "ClientSlashCommand",
    "ClientUser",
    "ClientUserCommand",
    "Color",
    "Colour",
    "CommandUtils",
    "Connectable",
    "CustomIdIsTooBig",
    "DMChannel",
    "DisallowedIntents",
    "DiscordAPIError",
    "DiscordGatewayWebsocket",
    "DiscordWSMessage",
    "Embed",
    "Emoji",
    "EpikCordException",
    "Event",
    "EventHandler",
    "FailedCheck",
    "FailedToConnectToVoice",
    "File",
    "Flag",
    "Forbidden403",
    "GateawayUnavailable502",
    "GatewayCECode",
    "GatewayOpcode",
    "Guild",
    "GuildApplicationCommandPermission",
    "GuildBan",
    "GuildChannel",
    "GuildManager",
    "GuildMember",
    "GuildNewsChannel",
    "GuildNewsThread",
    "GuildPreview",
    "GuildScheduledEvent",
    "GuildStageChannel",
    "GuildTextChannel",
    "GuildWidget",
    "GuildWidgetSettings",
    "HTTPClient",
    "IntegerOption",
    "Integration",
    "IntegrationAccount",
    "Intents",
    "InternalServerError5xx",
    "InvalidApplicationCommandOptionType",
    "InvalidApplicationCommandType",
    "InvalidArgumentType",
    "InvalidComponentStyle",
    "InvalidData",
    "InvalidIntents",
    "InvalidOption",
    "InvalidStatus",
    "InvalidToken",
    "Invite",
    "LabelIsTooBig",
    "List",
    "Locale",
    "Localisation",
    "Localization",
    "LocatedError",
    "MentionableOption",
    "MentionedChannel",
    "MentionedUser",
    "Message",
    "MessageActivity",
    "MessageCommandInteraction",
    "MessageComponentInteraction",
    "MessageInteraction",
    "Messageable",
    "MethodNotAllowed405",
    "MissingClientSetting",
    "MissingCustomId",
    "Modal",
    "ModalSubmitInteraction",
    "NotFound404",
    "NumberOption",
    "Overwrite",
    "Paginator",
    "PartialEmoji",
    "PartialGuild",
    "PartialUser",
    "Permissions",
    "Presence",
    "PrivateThread",
    "Ratelimited429",
    "Reaction",
    "ResolvedDataHandler",
    "Role",
    "RoleOption",
    "RoleTag",
    "Section",
    "SelectMenu",
    "SelectMenuOption",
    "Shard",
    "ShardManager",
    "ShardingRequired",
    "SlashCommand",
    "SlashCommandOptionChoice",
    "SourceChannel",
    "Status",
    "Sticker",
    "StickerItem",
    "StringOption",
    "SubCommandGroup",
    "Subcommand",
    "SystemChannelFlags",
    "Team",
    "TeamMember",
    "TextInput",
    "Thread",
    "ThreadArchived",
    "ThreadMember",
    "TooManyComponents",
    "TooManySelectMenuOptions",
    "TypingContextManager",
    "Unauthorized401",
    "UnavailableGuild",
    "UnhandledEpikCordException",
    "Union",
    "UnknownBucket",
    "User",
    "UserCommandInteraction",
    "UserOption",
    "Utils",
    "VoiceChannel",
    "VoiceOpcode",
    "VoiceRegion",
    "VoiceState",
    "Webhook",
    "WebhookUser",
    "WebsocketClient",
    "WelcomeScreen",
    "WelcomeScreenChannel",
    "b64encode",
    "cache_manager",
    "channel_manager",
    "close_event_codes",
    "component_from_type",
    "components",
    "decode_rtp_packet",
    "exceptions",
    "generate_rtp_packet",
    "guilds_manager",
    "logger",
    "managers",
    "nacl",
    "opcodes",
    "options",
    "os",
    "partials",
    "perf_counter_ns",
    "roles_manager",
    "rtp_handler",
    "type_enums",
)
