from __future__ import annotations

import datetime
from typing import TYPE_CHECKING, List, Optional, TypedDict, Union

from typing_extensions import NotRequired

from .application import Application, IntegrationApplication
from .channels import AnyChannel, GuildStageChannel, Overwrite
from .flags import Permissions, SystemChannelFlags
from .partials import PartialGuild
from .presence import Activity, Presence, Status
from .sticker import Sticker
from .thread import Thread
from .type_enums import (
    GuildScheduledEventPrivacyLevel,
    GuildScheduledEventStatus,
    IntegrationExpireBehavior,
    Locale,
    NSFWLevel,
    PremiumTier,
    VerificationLevel,
)
from .user import User
from .utils import Utils
from .voice import VoiceState

if TYPE_CHECKING:
    import discord_typings


class UnavailableGuild:
    """
    The class representation of an UnavailableGuild.
    The Guild object should be given to use when the guild is available.
    """

    def __init__(self, data: discord_typings.UnavailableGuildData):
        self.data = data
        self.id: int = int(data["id"])
        self.unavailable: Optional[bool] = data.get("unavailable")


class Invite:
    def __init__(self, client, data: discord_typings.InviteData):
        self.code: str = data["code"]
        self.client = client
        self.guild: Optional[PartialGuild] = (
            PartialGuild(data["guild"]) if data.get("guild") else None
        )
        self.channel: Optional[AnyChannel] = (
            Utils(client).channel_from_type(data["channel"])  # type: ignore
            if data.get("channel")
            else None
        )
        self.inviter: Optional[User] = (
            User(self.client, data["inviter"]) if data.get("inviter") else None
        )
        self.target_type: Optional[int] = data.get("target_type")
        self.target_user: Optional[User] = (
            User(self.client, data["target_user"]) if data.get("target_user") else None
        )
        self.target_application: Optional[Application] = (
            Application(data["target_application"])
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
            GuildStageChannel(self.client, data["stage_instance"])
            if data.get("stage_instance")
            else None
        )
        self.guild_scheduled_event: Optional[GuildScheduledEvent] = (
            GuildScheduledEvent(self.client, data["guild_scheduled_event"])
            if data.get("guild_scheduled_event")
            else None
        )


class GuildMember(User):
    def __init__(self, client, data: discord_typings.GuildMemberData):
        super().__init__(client, data["user"])
        self.data: discord_typings.GuildMemberData = data  # type: ignore
        self.client = client
        self.nick: Optional[str] = data.get("nick")
        self.avatar: Optional[str] = data.get("avatar")
        self.role_ids: List[int] = [int(role) for role in data["roles"]]
        self.joined_at: datetime.datetime = datetime.datetime.fromisoformat(
            data["joined_at"]
        )
        self.premium_since: Optional[datetime.datetime] = datetime.datetime.fromisoformat(data["premium_since"]) if data.get("premium_since") else None  # type: ignore
        self.deaf: bool = data["deaf"]
        self.mute: bool = data["mute"]
        self.pending: Optional[bool] = data.get("pending")
        self.permissions: Optional[Permissions] = (
            Permissions(int(data["permissions"])) if data.get("permissions") else None
        )
        self.communication_disabled_until: Optional[datetime.datetime] = datetime.datetime.fromisoformat(data["communication_disabled_until"]) if data.get("communication_disabled_until") else None  # type: ignore # until my pr is merged


class GuildPreview:
    def __init__(self, client, data: discord_typings.GuildPreviewData):
        self.id: int = int(data["id"])
        self.client = client
        self.name: str = data["name"]
        self.icon: Optional[str] = data.get("icon")
        self.splash: Optional[str] = data.get("splash")
        self.discovery_splash: Optional[str] = data.get("discovery_splash")
        self.emojis: List[Emoji] = [Emoji(client, emoji) for emoji in data["emojis"]]
        self.features: List[discord_typings.GuildFeaturesData] = data["features"]
        self.approximate_member_count: int = data["approximate_member_count"]
        self.approximate_presence_count: int = data["approximate_presence_count"]
        self.stickers: List[Sticker] = [
            Sticker(self.client, sticker) for sticker in data["stickers"]
        ]


class Guild:
    def __init__(self, client, data: discord_typings.GuildCreateData):
        from .flags import SystemChannelFlags

        self.client = client
        self.data = data
        print(f"Data is of type {type(data)}")
        self.id: int = int(data["id"])
        self.name: str = data["name"]
        self.icon: Optional[str] = data.get("icon")
        self.icon_hash: Optional[str] = data.get("icon_hash")
        self.splash: Optional[str] = data.get("splash")
        self.channels: List[AnyChannel] = []
        self.discovery_splash: Optional[str] = data.get("discovery_splash")
        self.owner_id: int = int(data["owner_id"])
        self.permissions = Permissions(int(data.get("permissions", 0)))
        self.afk_channel_id: Optional[int] = int(data["afk_channel_id"]) if data.get("afk_channel_id") else None  # type: ignore
        self.afk_timeout: int = data["afk_timeout"]

        self.verification_level: VerificationLevel = VerificationLevel(
            data["verification_level"]
        )

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
            Role(client, {**role_data, "guild": self})  # type: ignore # TODO: Change this to a better method
            for role_data in data["roles"]
        ]
        self.emojis: List[Emoji] = [Emoji(client, emoji) for emoji in data["emojis"]]
        self.features: List[discord_typings.GuildFeaturesData] = data["features"]
        self.mfa_level: str = "NONE" if data.get("mfa_level") == 0 else "ELEVATED"
        self.application_id: Optional[str] = data.get("application_id")
        self.system_channel_id: Optional[int] = int(data["system_channel_id"]) if data.get("system_channel_id") else None  # type: ignore
        self.system_channel_flags: SystemChannelFlags = SystemChannelFlags(
            data["system_channel_flags"]
        )
        self.rules_channel_id: Optional[int] = int(data["rules_channel_id"])  # type: ignore
        self.max_presences: Optional[int] = data.get("max_presences")
        self.max_members: Optional[int] = data.get("max_members")
        self.vanity_url_code: Optional[str] = data.get("vanity_url_code")
        self.description: Optional[str] = data.get("description")
        self.banner: Optional[str] = data.get("banner")
        self.premium_tier: PremiumTier = PremiumTier(data["premium_tier"])
        self.premium_subscription_count: Optional[int] = data.get(
            "premium_subscription_count"
        )
        self.preferred_locale: Locale = Locale(data["preferred_locale"])
        self.public_updates_channel_id: Optional[int] = int(data["public_updates_channel_id"]) if data.get("public_updates_channel_id") else None  # type: ignore
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
            WelcomeScreen(data["welcome_screen"])
            if data.get("welcome_screen")
            else None
        )
        self.nsfw_level: NSFWLevel = NSFWLevel(data["nsfw_level"])
        self.stickers: Optional[List[Sticker]] = (
            [Sticker(self.client, sticker) for sticker in data["stickers"]]
            if data.get("stickers")
            else None
        )

        # Below are the extra attributes sent over the gateway

        self.joined_at: Optional[datetime.datetime] = (
            datetime.datetime.fromisoformat(data["joined_at"])  # type: ignore
            if data.get("joined_at")
            else None
        )
        self.large: Optional[bool] = data.get("large")
        self.unavailable: Optional[bool] = data.get("unavailable")
        self.member_count: Optional[int] = data.get("member_count")
        self.voice_states: Optional[List[VoiceState]] = (
            [VoiceState(client, voice_state) for voice_state in data["voice_states"]]  # type: ignore
            if data.get("voice_states")
            else None
        )
        self.members: Optional[List[GuildMember]] = (
            [GuildMember(client, member) for member in data["members"]]  # type: ignore
            if data.get("members")
            else None
        )

        if data.get("channels"):
            self.channels.extend(
                [
                    client.utils.channel_from_type(channel)
                    for channel in data["channels"]
                ]
            )

        if data.get("threads"):
            self.channels.extend(
                [Thread(self.client, thread) for thread in data["threads"]]
            )

        self.presences: Optional[List[Presence]] = (
            [
                Presence(activity=p["activities"][-1], status=Status(p["status"])) for p in data["presences"]  # type: ignore
            ]
            if data.get("presences")
            else None
        )
        self.stage_instances: List[GuildStageChannel] = [
            GuildStageChannel(client, channel)
            for channel in data.get("stage_instances", [])
        ]
        self.guild_scheduled_events: List[GuildScheduledEvent] = [
            GuildScheduledEvent(client, event)
            for event in data.get("guild_scheduled_events", [])
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
    ) -> Guild:
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
        response = await self.client.http.patch(
            f"/guilds/{self.id}", json=data, headers=headers, guild_id=self.id
        )
        guild_data = await response.json()

        return Guild(self.client, guild_data)

    async def fetch_guild_preview(self) -> GuildPreview:
        """Fetches the guild preview.

        Returns
        -------
        GuildPreview
            The guild preview.
        """
        res = await self.client.http.get(f"/guilds/{self.id}/preview", guild_id=self.id)

        data = await res.json()
        return GuildPreview(self.client, data)

    async def delete(self):
        await self.client.http.delete(f"/guilds/{self.id}", guild_id=self.id)

    async def fetch_channels(self) -> List[AnyChannel]:
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


class RoleTags:
    def __init__(self, data: discord_typings.RoleTagsData):
        self.bot_id: Optional[int] = int(data.get("bot_id"))  # type: ignore
        self.integration_id: Optional[int] = int(data.get("integration_id"))  # type: ignore
        self.premium_subscriber: bool = bool(data.get("premium_subscriber"))


class Role:
    def __init__(self, client, data: discord_typings.RoleData):
        self.data = data
        self.client = client
        self.id: int = int(data["id"])
        self.name: str = data["name"]
        self.color: int = data["color"]
        self.hoist: bool = data["hoist"]
        self.icon: Optional[str] = data.get("icon")
        self.unicode_emoji: Optional[str] = data.get("unicode_emoji")
        self.position: int = data["position"]
        self.permissions: Permissions = Permissions(
            int(data["permissions"])
        )  # TODO: Permissions
        self.managed: bool = data["managed"]
        self.mentionable: bool = data["mentionable"]
        self.tags: Optional[RoleTags] = (
            RoleTags(data["tags"]) if data.get("tags") else None
        )
        self.guild: Guild = data["guild"] if data.get("guild") else None


class EditEmojiData(TypedDict):
    name: NotRequired[str]
    reason: NotRequired[str]
    roles: NotRequired[Optional[List[int]]]


class Emoji:
    def __init__(self, client, data: discord_typings.EmojiData):
        self.client = client
        self.id: Optional[int] = int(data["id"])  # type: ignore
        self.name: Optional[str] = data.get("name")
        self.roles: List[Role] = (
            [
                Role(client, role_data)  # type: ignore # TODO: Attach Guild to this or it won't work.
                for role_data in data["roles"]
            ]
            if data.get("roles")
            else []
        )
        self.user: Optional[User] = (
            User(self.client, data["user"]) if data.get("user") else None
        )
        self.requires_colons: Optional[bool] = data.get("require_colons")
        self.guild_id: Optional[str] = data.get("guild_id")  # type: ignore # TODO: check if this is input later
        self.managed: Optional[bool] = data.get("managed")
        self.animated: Optional[bool] = data.get("animated")
        self.available: Optional[bool] = data.get("available")

    async def edit(
        self,
        *,
        name: Optional[str] = None,
        roles: Optional[List[Role]] = None,
        reason: Optional[str] = None,
    ):
        payload: EditEmojiData = {}
        headers = self.client.http.headers.copy()
        if reason:
            headers["X-Audit-Log-Reason"] = reason

        if name:
            payload["name"] = name

        if roles:
            payload["roles"] = [int(role.id) for role in roles]

        emoji = await self.client.http.patch(
            f"/guilds/{self.guild_id}/emojis/{self.id}", json=payload, headers=headers
        )
        return Emoji(self.client, emoji)

    async def delete(self, *, reason: Optional[str] = None):
        headers = self.client.http.headers.copy()
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        await self.client.http.delete(
            f"/guilds/{self.guild_id}/emojis/{self.id}", headers=headers
        )


class WelcomeScreenChannel:
    def __init__(self, data: discord_typings.WelcomeChannelData):
        self.channel_id: int = int(data["channel_id"])
        self.description: str = data["description"]
        self.emoji_id: Optional[int] = int(data["emoji_id"]) if data.get("emoji_id") else None  # type: ignore
        self.emoji_name: Optional[str] = data.get("emoji_name")


class WelcomeScreen:
    def __init__(self, data: discord_typings.WelcomeScreenData):
        self.description: Optional[str] = data.get("description")
        self.welcome_channels: List[WelcomeScreenChannel] = [
            WelcomeScreenChannel(welcome_channel)
            for welcome_channel in data["welcome_channels"]
        ]


class GuildWidgetSettings:
    def __init__(self, data: dict):
        self.enabled: bool = data["enabled"]
        self.channel_id: Optional[int] = (
            int(data["channel_id"]) if data.get("channel_id") else None
        )


class GuildWidget:
    def __init__(self, client, data: discord_typings.GuildWidgetData):
        self.client = client
        self.data = data
        self.id: int = int(data["id"])
        self.name: str = data["name"]
        self.instant_invite: Optional[str] = data["instant_invite"]
        self.channels: List[AnyChannel] = [
            self.client.utils.channel_from_type(channel)
            for channel in data.get("channels", [])
        ]
        self.users: List[User] = [User(client, user) for user in data["members"]]
        self.presence_count: int = data["presence_count"]


class GuildScheduledEventEntityMetadata:
    def __init__(self, data: discord_typings.GuildScheduledEventEntityMetadataData):
        self.location: Optional[str] = data.get("location")


class GuildScheduledEvent:
    def __init__(self, client, data: discord_typings.GuildScheduledEventData):
        self.client = client
        self.id: int = int(data["id"])
        self.guild_id: int = int(data["guild_id"])
        self.channel_id: Optional[int] = int(data["channel_id"]) if data.get("channel_id") else None  # type: ignore
        self.creator_id: Optional[int] = (
            int(data["creator_id"]) if data.get("creator_id") else None
        )
        self.name: str = data["name"]
        self.description: Optional[str] = data.get("description")
        self.scheduled_start_time: datetime.datetime = datetime.datetime.fromisoformat(
            data["scheduled_start_time"]
        )
        self.scheduled_end_time: Optional[datetime.datetime] = (
            datetime.datetime.fromisoformat(data["scheduled_end_time"])
            if data.get("scheduled_end_time")
            else None
        )
        self.privacy_level: GuildScheduledEventPrivacyLevel = (
            GuildScheduledEventPrivacyLevel(data["privacy_level"])
        )
        self.status = GuildScheduledEventStatus(data["status"])

        self.entity_type: str = (
            "STAGE_INSTANCE"
            if data.get("entity_type") == 1
            else "VOICE"
            if data.get("entity_type") == 2
            else "EXTERNAL"
        )
        self.entity_id: Optional[int] = int(data["entity_id"]) if data.get("entity_id") else None  # type: ignore
        self.entity_metadata: Optional[GuildScheduledEventEntityMetadata] = GuildScheduledEventEntityMetadata(data["entity_metadata"]) if data.get("entity_metadata") else None  # type: ignore
        self.creator: Optional[User] = (
            User(client, data["creator"]) if data.get("creator") else None
        )
        self.user_count: Optional[int] = data.get("user_count")


class IntegrationAccount:
    def __init__(self, data: discord_typings.IntegrationAccountData):
        self.id: str = data["id"]
        self.name: str = data["name"]


class GuildBan:
    def __init__(self, client, data: discord_typings.BanData):
        self.reason: Optional[str] = data.get("reason")
        self.client = client
        self.user: User = User(client, data["user"])


class Integration:
    def __init__(
        self,
        client,
        data: Union[
            discord_typings.StreamingIntegrationData,
            discord_typings.DiscordIntegrationData,
        ],
    ):
        self.id: str = str(data["id"])
        self.client = client
        self.name: str = data["name"]
        self.type: str = data["type"]

        self.enabled: Optional[bool] = data.get("enabled")  # type: ignore
        self.syncing: Optional[bool] = data.get("syncing")  # type: ignore
        self.role_id: Optional[int] = int(data["role_id"]) if data.get("role_id") else None  # type: ignore
        self.subscriber_count: Optional[int] = data.get("subscriber_count")  # type: ignore
        self.revoked: Optional[bool] = data.get("revoked")  # type: ignore
        self.enable_emoticons: Optional[bool] = data.get("enable_emoticons")  # type: ignore
        self.expire_grace_period: Optional[int] = data.get("expire_grace_period")  # type: ignore

        self.expire_behavior: Optional[IntegrationExpireBehavior] = (
            IntegrationExpireBehavior(data["expire_behavior"])  # type: ignore
            if data.get("expire_behavior")
            else None
        )
        self.user: Optional[User] = (
            User(client, data["user"]) if data.get("user") else None  # type: ignore
        )
        self.account: IntegrationAccount = IntegrationAccount(data["account"])
        self.synced_at: Optional[datetime.datetime] = (
            datetime.datetime.fromisoformat(data["synced_at"])  # type: ignore
            if data.get("synced_at")
            else None
        )
        self.application: Optional[IntegrationApplication] = (
            IntegrationApplication(client, data["application"])
            if data.get("application")
            else None
        )


__all__ = (
    "Guild",
    "UnavailableGuild",
    "Invite",
    "GuildMember",
    "GuildPreview",
    "Role",
    "RoleTags",
    "Emoji",
    "WelcomeScreenChannel",
    "WelcomeScreen",
    "GuildWidgetSettings",
    "GuildWidget",
    "GuildScheduledEvent",
    "IntegrationAccount",
    "Integration",
    "GuildBan",
)
