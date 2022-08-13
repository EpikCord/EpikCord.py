"""
NOTE: version string only in setup.cfg
"""
from __future__ import annotations

import datetime
from typing import (
    Optional,
    List,
    Union,
    TypeVar,
    DefaultDict,
)
from .client import *
from .managers import *
from .abstract import *
from .auto_moderation import *
from .application import *
from .channels import *
from .close_event_codes import *
from .colour import *
from .components import *
from .exceptions import *
from .flags import *
from .localizations import *
from .message import *
from .opcodes import *
from .options import *
from .partials import *
from .rtp_handler import *
from .status_code import *
from .sticker import *
from .thread import *
from .type_enums import *
from .utils import *
from .commands import *
from .webhooks import *
from .interactions import *

T = TypeVar("T")
logger = getLogger(__name__)

__version__ = "0.5.2"

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


class Connection:
    def __init__(self, data: dict):
        self.id: str = data["id"]
        self.name: str = data["name"]
        self.type: str = data["type"]
        self.revoked: Optional[bool] = data["revoked"]
        self.integrations: Optional[List[Integration]] = [
            Integration(data) for data in data.get("integrations", [])
        ]
        self.verified: bool = data["verified"]
        self.friend_sync: bool = data["friend_sync"]
        self.show_activity: bool = data["show_activity"]
        self.visibility: VisibilityType = VisibilityType(data["visibility"])


class AuthorizationInformation:
    def __init__(self, data: dict):
        self.application: Application = Application(data["application"])
        self.scopes: List[str] = data["scopes"]
        self.expires: datetime.datetime = datetime.datetime.fromisoformat(
            data["expires"]
        )
        self.user: Optional[User] = (
            User(self, data["user"]) if data.get("user") else None
        )

    def to_dict(self) -> dict:
        payload = {
            "application": self.application.to_dict(),
            "scopes": self.scopes,
            "expires": self.expires.isoformat(),
        }
        if self.user:
            payload["user"] = self.user.to_dict()

        return payload


class UserClient:
    """This class is meant to be used with an Access Token. Not a User Account Token. This does not support Self Bots."""

    def __init__(self, token: str, *, discord_endpoint: str):
        self.token = token
        self._http: HTTPClient = HTTPClient(
            headers={
                "Authorization": f"Bearer {token}",
                "User-Agent": f"DiscordBot (https://github.com/EpikCord/EpikCord.py {__version__})",
            },
            discord_endpoint=discord_endpoint,
        )
        self.application: Optional[Application] = None

    async def fetch_application(self):
        application = Application(
            await (await self._http.get("/oauth2/applications/@me")).json()
        )
        self.application: Optional[Application] = application
        return application

    async def fetch_authorization_information(self):
        data = await (await self._http.get("/oauth2/@me")).json()
        if self.application:
            data["application"] = self.application.to_dict()
        return AuthorizationInformation(data)

    async def fetch_connections(self) -> List[Connection]:
        data = await (await self._http.get("/users/@me/connections")).json()
        return [Connection(d) for d in data]

    async def fetch_guilds(
        self,
        *,
        before: Optional[str] = None,
        after: Optional[str] = None,
        limit: int = 200,
    ) -> List[PartialGuild]:
        params = {"limit": limit}

        if before:
            params["before"] = before
        if after:
            params["after"] = after

        data = await (await self._http.get("/users/@me/guilds", params=params)).json()

        return [PartialGuild(d) for d in data]


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
        if status not in {"online", "dnd", "idle", "invisible", "offline"}:
            raise InvalidStatus("That is an invalid status.")

        self.status = status if status != "offline" else "invisible"


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


class UnavailableGuild:
    """
    The class representation of an UnavailableGuild.
    The Guild object should be given to use when the guild is available.
    """

    def __init__(self, data):
        self.data = data
        self.id: str = data.get("id")
        self.available: bool = data.get("available")


class Guild:
    def __init__(self, client, data: dict):
        self.client = client
        self.data: dict = data
        self.id: str = data.get("id")
        self.name: str = data.get("name")
        self.icon: Optional[str] = data.get("icon")
        self.icon_hash: Optional[str] = data.get("icon_hash")
        self.splash: Optional[str] = data.get("splash")
        self.discovery_splash: Optional[str] = data.get("discovery_splash")
        self.owner_id: str = data.get("owner_id")
        self.permissions = Permissions(int(data.get("permissions", 0)))
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
            Role(client, {**role_data, "guild": self})
            for role_data in data.get("roles")
        ]
        self.emojis: List[Emoji] = [
            Emoji(client, emoji, self.id) for emoji in data.get("emojis")
        ]
        self.features: List[str] = data.get("features")
        self.mfa_level: str = "NONE" if data.get("mfa_level") == 0 else "ELEVATED"
        self.application_id: Optional[str] = data.get("application_id")
        self.system_channel_id: Optional[str] = data.get("system_channel_id")
        self.system_channel_flags: int = SystemChannelFlags(
            data.get("system_channel_flags")
        )
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
        self.channels.extend(
            [Thread(self.client, thread) for thread in data.get("threads")]
        )
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
        self.stickers: Optional[List[StickerItem]] = (
            [StickerItem(sticker) for sticker in data.get("stickers")]
            if data.get("stickers")
            else None
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
        reason: Optional[str]
            The reason for editing the guild.
        Returns
        -------
        :class:`EpikCord.Guild`
        """
        data = Utils.filter_values(
            {
                "name": name,
                "verification_level": verification_level,
                "default_message_notifications": default_message_notifications,
                "explicit_content_filter": explicit_content_filter,
                "afk_channel_id": afk_channel_id,
                "afk_timeout": afk_timeout,
                "owner_id": owner_id,
                "system_channel_id": system_channel_id,
                "system_channel_flags": (
                    system_channel_flags.id if system_channel_flags else None
                ),
                "rules_channel_id": rules_channel_id,
                "preferred_locale": preferred_locale,
                "features": features,
                "description": description,
                "premium_progress_bar_enabled": premium_progress_bar_enabled,
            }
        )

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
        channels_ = await self.client.http.get(
            f"/guilds/{self.id}/channels", guild_id=self.id
        )
        return [self.client.utils.channel_from_type(channel) for channel in channels_]

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
        permission_overwrites: Optional[List[Overwrite]] = None,
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
        permission_overwrites: Optional[List[Overwrite]]
            The permission overwrites of the channel.
        parent_id: Optional[str]
            The parent id of the channel.
        nsfw: Optional[bool]
            Whether the channel is nsfw.
        """
        data = Utils.filter_values(
            {
                "name": name,
                "type": type,
                "topic": topic,
                "bitrate": bitrate,
                "user_limit": user_limit,
                "rate_limit_per_user": rate_limit_per_user,
                "position": position,
                "permission_overwrites": permission_overwrites,
                "parent_id": parent_id,
                "nsfw": nsfw,
            }
        )

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


class UnavailableGuild:
    """
    The class representation of an UnavailableGuild.
    The Guild object should be given to use when the guild is available.
    """

    def __init__(self, data):
        self.data = data
        self.id: str = data.get("id")
        self.available: bool = data.get("available")


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
        # * the user's banner color encoded as an integer representation of
        # * hexadecimal color code
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

class Overwrite:
    def __init__(self, data: dict):
        self.id: str = data.get("id")
        self.type: int = data.get("type")
        self.allow: str = data.get("allow")
        self.deny: str = data.get("deny")


class ThreadMember:
    def __init__(self, data: dict):
        self.id: str = data.get("user_id")
        self.thread_id: str = data.get("thread_id")
        self.join_timestamp: datetime.datetime = datetime.datetime.fromisoformat(
            data["join_timestamp"]
        )
        self.flags: int = data.get("flags")


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

    def to_dict(self) -> Dict[str, Any]:
        return Utils.filter_values(
            {
                "id": self.id,
                "filename": self.file_name,
                "description": self.description,
                "content_type": self.content_type,
                "size": self.size,
                "url": self.url,
                "proxy_url": self.proxy_url,
                "width": self.width,
                "height": self.height,
                "ephemeral": self.ephemeral,
            }
        )


class Section:
    _cmd = Union[ClientUserCommand, ClientSlashCommand, ClientMessageCommand]

    _commands: DefaultDict[str, List[_cmd]] = defaultdict(list)
    _events: DefaultDict[str, List[Event]] = defaultdict(list)

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


# class ClientGuildMember(Member):
#     def __init__(self, client: Client,data: dict):
#         super().__init__(data)


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
            Role(client, {**role_data, "guild": self})
            for role_data in data.get("roles")
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

        self.status = {
            "SCHEDULED": 1,
            "ACTIVE": 2,
            "COMPLETED": 3,
        }.get(data.get("status"), "CANCELLED")

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
        self.allowed_mentions: List[str] = allowed_mentions
        self.replied_user: bool = replied_user
        self.roles: List[str] = roles
        self.users: List[str] = users

    def to_dict(self) -> Dict[str, Any]:
        return {
            "allowed_mentions": self.allowed_mentions,
            "replied_user": self.replied_user,
            "roles": self.roles,
            "users": self.users,
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
        opts = [
            Subcommand,
            SubCommandGroup,
            StringOption,
            IntegerOption,
            BooleanOption,
            UserOption,
            ChannelOption,
            RoleOption,
            MentionableOption,
            NumberOption,
            AttachmentOption,
        ]

        for option in self.options:
            option_type = option.get("type")
            if option_type >= len(opts):
                raise ValueError(f"Invalid option type {option_type}")

            # shouldn't be return but since it was return before I'll leave it
            return opts[option_type - 1](option)

    def to_dict(self):
        json_options = [option.to_dict for option in self.options]
        return {
            "name": self.name,
            "type": self.type,
            "description": self.description,
            "options": json_options,
        }


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

    async def ready(self, data: dict):
        self.user: ClientUser = ClientUser(self, data.get("user"))
        self.session_id: str = data["session_id"]
        application_response = await self.http.get("/oauth2/applications/@me")
        application_data = await application_response.json()
        self.application: ClientApplication = ClientApplication(self, application_data)
        return None

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


class ShardManager(EventHandler):
    def __init__(
        self,
        token: str,
        intents: Optional[Union[Intents, int]],
        *,
        shards: Optional[int] = None,
        overwrite_commands_on_ready: bool = False,
    ):
        super().__init__()
        self.token: str = token
        self.overwrite_commands_on_ready: bool = overwrite_commands_on_ready
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
                shard.events = self.events
                coro = shard.wait_for("ready")
                await shard.login()
                await coro()

                current_iteration += 1

                if current_iteration == max_concurrency:
                    await asyncio.sleep(5)
                    current_iteration = 0  # Reset it

            if self.overwrite_commands_on_ready:
                for shard in self.shards:
                    await Utils(shard).override_commands()

        loop = asyncio.get_event_loop()
        loop.run_until_complete(wrapper())

__all__ = (
    "__version__",
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
    "opcodes",
    "options",
    "partials",
    "roles_manager",
    "rtp_handler",
    "type_enums",
)
