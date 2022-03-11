import datetime
from .application import Application
from .channel import GuildChannel, WelcomeScreen, GuildStageChannel, Overwrite
from .client import Client
from .emoji import Emoji 
from .guild import GuildPreview
from .role import Role
from .sticker import StickerItem, Sticker
from .thread import Thread
from .member import GuildMember, User
from .ext import SystemChannelFlags
from typing import Optional, List


class Guild:
    def __init__(self, client: Client, data: dict):
        self.client = client
        self.data: dict = data
        self.id: str = data.get("id")
        self.name: str = data.get("name")
        self.icon: Optional[str] = data.get("icon")
        self.icon_hash: Optional[str] = data.get("icon_hash")
        self.splash: Optional[str] = data.get("splash")
        self.discovery_splash: Optional[str] = data.get("discovery_splash")
        self.owner_id: str = data.get("owner_id")
        self.permissions: str = data.get("permissions")
        self.afk_channel_id: str = data.get("afk_channel_id")
        self.afk_timeout: int = data.get("afk_timeout")
        self.verification_level: str = "NONE" if data.get("verification_level") == 0 else "LOW" if data.get("verification_level") == 1 else "MEDIUM" if data.get("verification_level") == 2 else "HIGH" if data.get("verification_level") == 3 else "VERY_HIGH"
        self.default_message_notifications: str = "ALL" if data.get("default_message_notifications") == 0 else "MENTIONS"
        self.explicit_content_filter: str = "DISABLED" if data.get("explicit_content_filter") == 0 else "MEMBERS_WITHOUT_ROLES" if data.get("explicit_content_filter") == 1 else "ALL_MEMBERS"
        self.roles: List[Role] = [Role(role) for role in data.get("roles")]
        self.emojis: List[Emoji] = [Emoji(emoji) for emoji in data.get("emojis")]
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
        self.members: List[GuildMember] = [GuildMember(member) for member in data.get("members")]
        self.channels: List[GuildChannel] = [GuildChannel(channel) for channel in data.get("channels")]
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
        self.public_updates_channel_id: Optional[str] = data.get("public_updates_channel_id")
        self.max_video_channel_users: Optional[int] = data.get("max_video_channel_users")
        self.approximate_member_count: Optional[int] = data.get("approximate_member_count")
        self.approximate_presence_count: Optional[int] = data.get("approximate_presence_count")
        self.welcome_screen: Optional[WelcomeScreen] = WelcomeScreen(data.get("welcome_screen")) if data.get("welcome_screen") else None
        self.nsfw_level: int = data.get("nsfw_level")
        self.stage_instances: List[GuildStageChannel] = [GuildStageChannel(channel) for channel in data.get("stage_instances")]
        self.stickers: Optional[StickerItem] = StickerItem(data.get("stickers")) if data.get("stickers") else None
        self.guild_schedulded_events: List[GuildScheduledEvent] = [GuildScheduledEvent(event) for event in data.get("guild_schedulded_events", [])]

    async def edit(self, *, name: Optional[str] = None, verification_level: Optional[int] = None, default_message_notifications: Optional[int] = None, explicit_content_filter: Optional[int] = None, afk_channel_id: Optional[str] = None, afk_timeout: Optional[int] = None, owner_id: Optional[str] = None, system_channel_id: Optional[str] = None, system_channel_flags: Optional[SystemChannelFlags] = None, rules_channel_id: Optional[str] = None, preferred_locale: Optional[str] = None, features: Optional[List[str]] = None, description: Optional[str] = None, premium_progress_bar_enabled: Optional[bool] = None, reason: Optional[str] = None):
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
        return Guild(await self.client.http.patch(f"/guilds/{self.id}", json=data, headers=headers))
    
    async def fetch_guild_preview(self) -> GuildPreview:
        """Fetches the guild preview.

        Returns
        -------
        GuildPreview
            The guild preview.
        """
        if getattr(self, "preview"):
            return self.preview

        preview = GuildPreview(await self.client.http.get(f"/guilds/{self.id}/preview"))
        return preview
    
    async def delete(self):
        await self.client.http.delete(f"/guilds/{self.id}")
    
    async def fetch_channels(self) -> List[GuildChannel]:
        """Fetches the guild channels.

        Returns
        -------
        List[GuildChannel]
            The guild channels.
        """
        channels = await self.client.http.get(f"/guilds/{self.id}/channels")
        return_channels = []
        for channel in channels:
            return_channels.append(self.client.utils._figure_out_channel_type(channel))
        
        return return_channels
    
    async def create_channel(self, *, name: str, reason: Optional[str] = None, type: Optional[int] = None, topic: Optional[str] = None, bitrate: Optional[int] = None, user_limit: Optional[int] = None, rate_limit_per_user: Optional[int] = None, position: Optional[int] = None, permission_overwrites: List[Optional[Overwrite]] = None, parent_id: Optional[str] = None, nsfw: Optional[bool] = None):
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

        return _figure_out_channel_type(await self.client.http.post(f"/guilds/{self.id}/channels", json=data, headers=headers))

class UnavailableGuild:

    def __init__(self, data):
        self.data = data
        self.id: str = data.get("id")
        self.available: bool = data.get("available")

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
        self.sticekrs: List[Sticker] = [Sticker(sticker) for sticker in data.get("stickers", [])]

class GuildWidgetSettings:
    def __init__(self, data: dict):
        self.enabled: bool = data.get("enabled")
        self.channel_id: Optional[str] = data.get("channel_id")

class GuildWidget:
    def __init__(self, data: dict):
        self.id: str = data.get("id")
        self.name: str = data.get("name")
        self.instant_invite: str = data.get("instant_invite")
        self.channels: List[GuildChannel] = [GuildChannel(channel) for channel in data.get("channels", [])]
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
        self.status: str = "SCHEDULED" if data.get("status") == 1 else "ACTIVE" if data.get("status") == 2 else "COMPLETED" if data.get("status") == 3 else "CANCELLED"
        self.entity_type: str = "STAGE_INSTANCE" if data.get("entity_type") == 1 else "VOICE" if data.get("entity_type") == 2 else "EXTERNAL"
        self.entity_id: str = data.get("entity_id")
        self.entity_metadata: dict = data.get("entity_metadata")
        self.creator: Optional[User] = User(data.get("creator"))
        self.user_count: Optional[int] = data.get("user_count")



class GuildBan:
    def __init__(self, data: dict):
        self.reason: Optional[str] = data.get("reason")
        self.user: User = User(data.get("user"))

class PartialGuild:
    def __init__(self, data):
        self.data: dict = data
        self.id: str = data.get("id")
        self.name: str = data.get("name")
        self.permissions: int = int(data.get("permissions"))
        self.features: List[str] = data.get("features")

class IntegrationAccount:
    def __init__(self, data: dict):
        self.id: str = data.get("id")
        self.name: str = data.get("name")

class Integration:
    def __init__(self, data: dict):
        self.id: str = data.get("id")
        self.name: str = data.get("name")
        self.type: str = data.get("type")
        self.enabled: bool = data.get("enabled")
        self.syncing: Optional[bool] = data.get("syncing")
        self.role_id: Optional[str] = data.get("role_id")
        self.expire_behavior: str = "REMOVE_ROLE" if data.get("expire_behavior") == 1 else "REMOVE_ACCOUNT" if data.get("expire_behavior") == 2 else None
        self.expire_grace_period: Optional[int] = data.get("expire_grace_period")
        self.user: Optional[User] = User(data.get("user")) if data.get("user") else None
        self.account: IntegrationAccount = IntegrationAccount(data.get("account"))
        self.synced_at: datetime.datetime = datetime.datetime.fromioformat(data.get("synced_at"))
        self.subscriber_count: int = data.get("subscriber_count")
        self.revoked: bool = data.get("revoked")
        self.application: Optional[Application] = Application(data.get("application")) if data.get("application") else None
