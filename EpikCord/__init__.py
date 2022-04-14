"""
NOTE: __version__ in this file, __main__ and setup.cfg
"""


from .managers import *
from aiohttp import *
import asyncio
from base64 import b64encode
import datetime
import re
from logging import getLogger
from typing import *
from urllib.parse import quote
import io
import os

logger = getLogger(__name__)
__version__ = '0.4.13.3'


"""
:license:
Some parts of the code is sourced from discord.py
The MIT License (MIT)
Copyright © 2015-2021 Rapptz
Copyright © 2021-present EpikHost
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, RESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE."""
class Status:
    def __init__(self, status: str):
        
        if status in {"online", "dnd", "idle", "invisible", "offline"}:
            setattr(self, "status", status if status != "offline" else "invisible")
        else:
            raise InvalidStatus("That is an invalid status.")


class Activity:
    """_summary_
    Represents an Discord Activity object.
    :param name: The name of the activity.
    :param type: The type of the activity.
    :param url: The url of the activity (if its a stream).
    
    """
    def __init__(self, *, name: str, type: int, url: Optional[str] = None):
        self.name = name
        self.type = type
        self.url = url

    def to_dict(self):
        """Returns activity class as dict

        Returns:
            dict: returns :class:`dict` of :class:`activity`
        """
        return {
            "name": self.name,
            "type": self.type,
            "url": self.url
        }

class Presence:
    def __init__(self, *, since: Optional[int] = None, activities: Optional[List[Activity]] = None, status: Optional[Status] = None, afk: Optional[bool] = None):
        self.since: Optional[int] = since or None
        self.activities: Optional[List[Activity]] = activities or None
        self.status: Status = status.status if status else None
        self.afk: Optional[bool] = afk or None

    def to_dict(self):
        payload = {}
        if self.since:
            payload["since"] = self.since
        if self.activities:
            payload["activities"] = [activity.to_dict() for activity in self.activities]
        if self.afk:
            payload["afk"] = self.afk
        if self.status:
            payload["status"] = self.status
        
        return payload

class UnavailableGuild:

    def __init__(self, data):
        self.data = data
        self.id: str = data.get("id")
        self.available: bool = data.get("available")

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
        # the user's banner color encoded as an integer representation of hexadecimal color code
        self.accent_color: Optional[int] = data.get("accent_color")
        self.locale: Optional[str] = data.get("locale")
        self.verified: bool = data.get("verified")
        self.email: Optional[str] = data.get("email")
        self.flags: int = data.get("flags")
        self.premium_type: int = data.get("premium_type")
        self.public_flags: int = data.get("public_flags")


class VoiceWebsocketClient:
    def __init__(self):
        self.ws = None
        # Work on later


class RatelimitHandler:
    """
    A class to handle ratelimits from Discord.
    """
    def __init__(self, *, avoid_ratelimits: Optional[bool] = True):
        self.ratelimit_buckets: dict = {}
        self.ratelimited: bool = False
        self.avoid_ratelimits: bool = avoid_ratelimits

    async def process_headers(self, headers: dict):
        """
        Read the headers from a request and then digest it.
        """
        if headers.get("X-Ratelimit-Bucket"):

            self.ratelimit_buckets[headers["X-Ratelimit-Bucket"]] = {
                "limit": headers["X-Ratelimit-Limit"],
                "remaining": headers["X-Ratelimit-Remaining"],
                "reset": headers["X-Ratelimit-Reset"]
            }

        if headers["X-Ratelimit-Remaining"] == 1 and self.avoid_ratelimits:
            logger.critical("You have been nearly been ratelimited. We're now pausing requests.")
            self.ratelimited = True
            await asyncio.sleep(headers["X-Ratelimit-Reset-After"])
            self.ratelimited = False

        if headers.get("X-Ratelimit-Global") or headers.get("X-Ratelimit-Scope"):
            logger.critical("You have been ratelimited. You've reached a 429. We're now pausing requests.")
            self.ratelimited = True
            await asyncio.sleep(headers["retry_after"])
            self.ratelimited = False

    def is_ratelimited(self) -> bool:
        """
        Checks if the client is ratelimited.
        """
        return self.ratelimited

class HTTPClient(ClientSession):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, raise_for_status = True)
        self.base_uri: str = "https://discord.com/api/v9"
        self.ratelimit_handler = RatelimitHandler(avoid_ratelimits = kwargs.get("avoid_ratelimits", False))
    
    async def log_request(self, res):
        message = f"Sent a {res.request_info.method} to {res.url} and got a {res.status} response. "
        if await res.json():
            message += f"Received body: {await res.json()} "
        if dict(res.headers):
            message += f"Received headers: {dict(res.headers)} "
        if dict(res.request_info.headers):
            message += f"Sent headers: {dict(res.request_info.headers)} "
        logger.debug(message)

    async def get(self, url, *args, to_discord: bool = True, **kwargs):
        if to_discord:
            if self.ratelimit_handler.is_ratelimited():
                return

            if url.startswith("/"):
                url = url[1:]

            res = await super().get(f"{self.base_uri}/{url}", *args, **kwargs)
            await self.log_request(res)
            return res
        return await super().get(url, *args, **kwargs)

    async def post(self, url, *args, to_discord: bool = True, **kwargs):
        if to_discord:
            if self.ratelimit_handler.is_ratelimited():
                return

            if url.startswith("/"):
                url = url[1:]

            res = await super().post(f"{self.base_uri}/{url}", *args, **kwargs)
            await self.log_request(res)
            return res
        
        return await super().post(url, *args, **kwargs)

    async def patch(self, url, *args, to_discord: bool = True, **kwargs):
        if to_discord:
            if self.ratelimit_handler.is_ratelimited():
                return

            if url.startswith("/"):
                url = url[1:]

            res = await super().patch(f"{self.base_uri}/{url}", *args, **kwargs)
            await self.log_request(res)
            return res
        return await super().patch(url, *args, **kwargs)

    async def delete(self, url, *args, to_discord: bool = True, **kwargs):
        if to_discord:
            if self.ratelimit_handler.is_ratelimited():
                return

            if url.startswith("/"):
                url = url[1:]

            res = await super().delete(f"{self.base_uri}/{url}", *args, **kwargs)
            await self.log_request(res)
            return res
        return await super().delete(url, *args, **kwargs)

    async def put(self, url, *args, to_discord: bool = True, **kwargs):
        if to_discord:
                
            if self.ratelimit_handler.is_ratelimited():
                return

            if url.startswith("/"):
                url = url[1:]

            res = await super().put(f"{self.base_uri}/{url}", *args, **kwargs)
            await self.log_request(res)

            return res
        return await super().put(url, *args, **kwargs)

    async def head(self, url, *args, to_discord: bool = True, **kwargs):
        if to_discord:
            if self.ratelimit_handler.is_ratelimited():
                return

            if url.startswith("/"):
                url = url[1:]

            res =  await super().head(f"{self.base_uri}/{url}", *args, **kwargs)
            await self.log_request(res)

            return res
        return await super().head(url, *args, **kwargs)

 




# class ClientGuildMember(Member):
#     def __init__(self, client: Client,data: dict):
#         super().__init__(data)


class Embed:  # Always wanted to make this class :D
    def __init__(self, *,
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

    def set_thumbnail(self, *, url: Optional[str] = None, proxy_url: Optional[str] = None, height: Optional[int] = None, width: Optional[int] = None):
        config = {
            "url": url
        }
        if proxy_url:
            config["proxy_url"] = proxy_url
        if height:
            config["height"] = height
        if width:
            config["width"] = width

        self.thumbnail = config

    def set_video(self, *, url: Optional[str] = None, proxy_url: Optional[str] = None, height: Optional[int] = None, width: Optional[int] = None):
        config = {
            "url": url
        }
        if proxy_url:
            config["proxy_url"] = proxy_url
        if height:
            config["height"] = height
        if width:
            config["width"] = width

        self.video = config

    def set_image(self, *, url: Optional[str] = None, proxy_url: Optional[str] = None, height: Optional[int] = None, width: Optional[int] = None):
        config = {
            "url": url
        }
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

    def set_footer(self, *, text: Optional[str], icon_url: Optional[str] = None, proxy_icon_url: Optional[str] = None):
        payload = {}
        if text:
            payload["text"] = text
        if icon_url:
            payload["icon_url"] = icon_url
        if proxy_icon_url:
            payload["proxy_icon_url"] = proxy_icon_url
        self.footer = payload

    def set_author(self, name: Optional[str] = None, url: Optional[str] = None, icon_url: Optional[str] = None, proxy_icon_url: Optional[str] = None):
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

        if getattr(self, "title"):
            final_product["title"] = self.title
        if getattr(self, "description"):
            final_product["description"] = self.description
        if getattr(self, "url"):
            final_product["url"] = self.url
        if getattr(self, "timestamp"):
            final_product["timestamp"] = self.timestamp
        if getattr(self, "color"):
            final_product["color"] = self.color
        if getattr(self, "footer"):
            final_product["footer"] = self.footer
        if getattr(self, "image"):
            final_product["image"] = self.image
        if getattr(self, "thumbnail"):
            final_product["thumbnail"] = self.thumbnail
        if getattr(self, "video"):
            final_product["video"] = self.video
        if getattr(self, "provider"):
            final_product["provider"] = self.provider
        if getattr(self, "author"):
            final_product["author"] = self.author
        if getattr(self, "fields"):
            final_product["fields"] = self.fields

        return final_product


class RoleTag:
    def __init__(self, data: dict):
        self.bot_id: Optional[str] = data.get("bot_id")
        self.integration_id: Optional[str] = data.get("integration_id")
        self.premium_subscriber: Optional[bool] = data.get(
            "premium_subscriber")


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


class Emoji:
    def __init__(self, client, data: dict, guild_id: str):
        self.client = client
        self.id: Optional[str] = data.get("id")
        self.name: Optional[str] = data.get("name")
        self.roles: List[Role] = [Role(role) for role in data.get("roles", [])]
        self.user: Optional[User] = User(data.get("user")) if "user" in data else None
        self.requires_colons: bool = data.get("require_colons")
        self.guild_id: str = data.get("guild_id")
        self.managed: bool = data.get("managed")
        self.guild_id: str = guild_id
        self.animated: bool = data.get("animated")
        self.available: bool = data.get("available")

    async def edit(self, *, name: Optional[str] = None, roles: Optional[List[Role]] = None, reason: Optional[str] = None):
        payload = {}

        if reason:
            payload["X-Audit-Log-Reason"] = reason

        if name:
            payload["name"] = name

        if roles:
            payload["roles"] = [role.id for role in roles]

        emoji = await self.client.http.patch(f"/guilds/{self.guild_id}/emojis/{self.id}", json=payload)
        return Emoji(self.client, emoji, self.guild_id)

    async def delete(self, *, reason: Optional[str] = None):
        payload = {}

        if reason:
            payload["X-Audit-Log-Reason"] = reason

        await self.client.http.delete(f"/guilds/{self.guild_id}/emojis/{self.id}", json=payload)

class WelcomeScreenChannel:
    def __init__(self, data: dict):
        self.channel_id: str = data.get("channel_id")
        self.description: str = data.get("description")
        self.emoji_id: Optional[str] = data.get("emoji_id")
        self.emoji_name: Optional[str] = data.get("emoji_name")


class WelcomeScreen:
    def __init__(self, data: dict):
        self.description: Optional[str] = data.get("description")
        self.welcome_channels: List[WelcomeScreenChannel] = [WelcomeScreenChannel(welcome_channel) for welcome_channel in data.get("welcome_channels")]

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
        self.stickers: List[Sticker] = [Sticker(sticker) for sticker in data.get("stickers", [])]

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
        self.expire_behavior: str = "REMOVE_ROLE" if data.get("expire_behavior") == 1 else "REMOVE_ACCOUNT" if data.get("expire_behavior") == 2 else None
        self.expire_grace_period: Optional[int] = data.get("expire_grace_period")
        self.user: Optional[User] = User(data.get("user")) if data.get("user") else None
        self.account: IntegrationAccount = IntegrationAccount(data.get("account"))
        self.synced_at: datetime.datetime = datetime.datetime.fromioformat(data.get("synced_at"))
        self.subscriber_count: int = data.get("subscriber_count")
        self.revoked: bool = data.get("revoked")
        self.application: Optional[Application] = Application(data.get("application")) if data.get("application") else None

def _figure_out_channel_type(client, channel):
    channel_type = channel["type"]
    if channel_type == 0:
        return GuildTextChannel(client, channel)
    elif channel_type == 1:
        return DMChannel(client, channel)
    elif channel_type == 2:
        return VoiceChannel(client, channel)
    elif channel_type == 4:
        return ChannelCategory(client, channel)
    elif channel_type == 5:
        return GuildNewsChannel(client, channel)
    elif channel_type == 6:
        return GuildStoreChannel(client, channel)
    elif channel_type == 10:
        return GuildNewsThread(client, channel)
    elif  channel_type in (11, 12):
        return Thread(client, channel)
    elif channel_type == 13:
        return GuildStageChannel(client, channel)
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

        return GuildPreview(await self.client.http.get(f"/guilds/{self.id}/preview"))
    
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
        return [_figure_out_channel_type(channel) for channel in channels]
    
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

class WebhookUser:
    def __init__(self, data: dict):
        self.webhook_id: str = data.get("webhook_id")
        self.username: str = data.get("username")
        self.avatar: str = data.get("avatar")


class Webhook:
    def __init__(self, client, data: dict = None):
        """
        Don't pass in data if you're making a webhook, the lib passes data to construct an already existing webhook
        """
        self.client = client
        self.data = data
        if data:
            self.id: str = data.get("id")
            self.type: str = "Incoming" if data.get(
                "type") == 1 else "Channel Follower" if data.get("type") == 2 else "Application"
            self.guild_id: Optional[str] = data.get("guild_id")
            self.channel_id: Optional[str] = data.get("channel_id")
            self.user: Optional[User] = User(client, data.get("user"))
            self.name: Optional[str] = data.get("name")
            self.avatar: Optional[str] = data.get("avatar")
            self.token: Optional[str] = data.get("token")
            self.application_id: Optional[str] = data.get("application_id")
            self.source_guild: Optional[PartialGuild] = PartialGuild(
                data.get("source_guild"))
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
            "components": self.components
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
        self.author: Union[User, GuildMember] = GuildMember(client, data.get("member")) if data.get("member") else User(client, data.get("user"))
        self.token: str = data.get("token")
        self.version: int = data.get("version")
        self.locale: Optional[str] = data.get("locale")
        self.guild_locale: Optional[str] = data.get("guild_locale")
        self.original_response: Optional[Message] = None # Can't be set on construction.
        self.followup_response: Optional[Message] = None # Can't be set on construction.

    async def reply(self, *, tts: bool = False, content: Optional[str] = None, embeds: Optional[List[Embed]] = None, allowed_mentions = None, components: Optional[List[Union[Button, SelectMenu, TextInput]]] = None, attachments: Optional[List[Attachment]] = None, suppress_embeds: Optional[bool] = False, ephemeral: Optional[bool] = False) -> None:

        message_data = {
            "tts": tts,
            "flags": 0
        }

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
            message_data["components"] = [component.to_dict() for component in components]
        if attachments:
            message_data["attachments"] = [attachment.to_dict() for attachment in attachments]

        payload = {
            "type": 4,
            "data": message_data
        }
        await self.client.http.post(f"/interactions/{self.id}/{self.token}/callback", json = payload)
    
    async def defer(self, *, show_loading_state: Optional[bool] = True):
        if show_loading_state:
            return await self.client.http.post(f"/interaction/{self.id}/{self.token}/callback", json = {"type": 5})
        else:
            return await self.client.http.post(f"/interaction/{self.id}/{self.token}/callback", json = {"type": 6})

    async def send_modal(self, modal: Modal):
        if not isinstance(modal, Modal):
            raise InvalidArgumentType("The modal argument must be of type Modal.")
        payload = {
            "type": 9,
            "data": modal.to_dict()
        }
        await self.client.http.post(f"/interactions/{self.id}/{self.token}/callback", json=payload)

    def is_ping(self):
        return self.type == 1

    def is_application_command(self):
        return self.type == 2

    def is_message_component(self):
        return self.type == 3

    def is_autocomplete(self):
        return self.type == 4
    
    def is_modal_submit(self):
        return self.type == 5

    async def fetch_original_response(self, *, skip_cache: Optional[bool] = False):
        if not skip_cache and self.original_response:
            return self.original_response
        message_data = await self.client.http.get(f"/webhooks/{self.application_id}/{self.token}/messages/@original")
        self.original_response: Message = Message(self.client, message_data)
        return self.original_response
    
    async def edit_original_response(self, *, tts: bool = False, content: Optional[str] = None, embeds: Optional[List[Embed]] = None, allowed_mentions = None, components: Optional[List[Union[Button, SelectMenu, TextInput]]] = None, attachments: Optional[List[Attachment]] = None, suppress_embeds: Optional[bool] = False, ephemeral: Optional[bool] = False) -> None:

        message_data = {
            "tts": tts,
            "flags": 0
        }

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
            message_data["components"] = [component.to_dict() for component in components]
        if attachments:
            message_data["attachments"] = [attachment.to_dict() for attachment in attachments]

        new_message_data = await self.client.http.patch(f"/webhooks/{self.application_id}/{self.token}/messages/@original", json = message_data)
        self.original_response: Message = Message(self.client, new_message_data)
        return self.original_response
    
    async def delete_original_response(self):
        await self.client.http.delete(f"/webhooks/{self.application_id}/{self.token}/messages/@original")

    async def create_followup(self, *, tts: bool = False, content: Optional[str] = None, embeds: Optional[List[Embed]] = None, allowed_mentions = None, components: Optional[List[Union[Button, SelectMenu, TextInput]]] = None, attachments: Optional[List[Attachment]] = None, suppress_embeds: Optional[bool] = False, ephemeral: Optional[bool] = False) -> None:

        message_data = {
            "tts": tts,
            "flags": 0
        }

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
            message_data["components"] = [component.to_dict() for component in components]
        if attachments:
            message_data["attachments"] = [attachment.to_dict() for attachment in attachments]

        response = await self.client.http.post(f"/webhooks/{self.application_id}/{self.token}", json = message_data)
        new_message_data = await response.json()
        self.followup_response: Message = Message(self.client, new_message_data)
        return self.followup_response

    async def edit_followup(self, *, tts: bool = False, content: Optional[str] = None, embeds: Optional[List[Embed]] = None, allowed_mentions = None, components: Optional[List[Union[Button, SelectMenu, TextInput]]] = None, attachments: Optional[List[Attachment]] = None, suppress_embeds: Optional[bool] = False, ephemeral: Optional[bool] = False) -> None:

        message_data = {
            "tts": tts,
            "flags": 0
        }

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
            message_data["components"] = [component.to_dict() for component in components]
        if attachments:
            message_data["attachments"] = [attachment.to_dict() for attachment in attachments]

        await self.client.http.patch(f"/webhook/{self.application_id}/{self.token}/", json = message_data)

    async def delete_followup(self):
        return await self.client.http.delete(f"/webhook/{self.application_id}/{self.token}/")

class MessageComponentInteraction(BaseInteraction):
    def __init__(self, client, data: dict):
        super().__init__(client, data)
        self.message: Message = Message(client, data.get("message"))
        self.custom_id: str = self.interaction_data.get("custom_id")
        self.component_type: Optional[int] = self.interaction_data.get("component_type")
        self.values: Optional[dict] = [SelectMenuOption(option) for option in self.interaction_data.get("values", [])]

    def is_action_row(self):
        return self.component_type == 1

    def is_button(self):
        return self.component_type == 2
    
    def is_select_menu(self):
        return self.component_type == 3

    def is_text_input(self):
        return self.component_type == 4

    async def update(self, *, tts: bool = False, content: Optional[str] = None, embeds: Optional[List[Embed]] = None, allowed_mentions = None, components: Optional[List[Union[Button, SelectMenu, TextInput]]] = None, attachments: Optional[List[Attachment]] = None, suppress_embeds: Optional[bool] = False) -> None:

        message_data = {
            "tts": tts,
            "flags": 0
        }

        if suppress_embeds:
            message_data["flags"] += 1 << 2

        if content:
            message_data["content"] = content
        if embeds:
            message_data["embeds"] = [embed.to_dict() for embed in embeds]
        if allowed_mentions:
            message_data["allowed_mentions"] = allowed_mentions.to_dict()
        if components:
            message_data["components"] = [component.to_dict() for component in components]
        if attachments:
            message_data["attachments"] = [attachment.to_dict() for attachment in attachments]

        payload = {
            "type": 7,
            "data": message_data
        }

        await self.client.http.patch(f"/interaction/{self.id}/{self.token}/callback", json = payload)

    async def defer_update(self):
        await self.client.http.post(f"/interaction/{self.id}/{self.token}/callback", json = {
            "type": 6
        })


class ModalSubmitInteraction(BaseInteraction):
    def __init__(self, client, data: dict):
        super().__init__(client, data)
        self.custom_id: str = self.interaction_data["custom_id"]
        self._components: List[Union[Button, SelectMenu, TextInput]] = self.interaction_data.get("components")

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
        self.options: List[ApplicationCommandOption] = [ApplicationCommandOption(option) for option in data.get("options", [])]

    async def reply(self, choices: List[SlashCommandOptionChoice]) -> None:
        payload = {
            "type": 9,
            "data": []
        }

        for choice in choices:
            if not isinstance(choice, SlashCommandOptionChoice):
                raise TypeError(f"{choice} must be of type SlashCommandOptionChoice")
            payload["data"]["choices"].append(choice.to_dict())

        await self.client.http.post(f"/interactions/{self.id}/{self.token}/callback", json = payload)

class ApplicationCommandSubcommandOption(ApplicationCommandOption):
    def __init__(self, data: dict):
        super().__init__(data)
        self.options: List[ApplicationCommandOption] = [ApplicationCommandOption(option) for option in data.get("options", [])]

class ResolvedDataHandler:
    def __init__(self, client, resolved_data: dict):
        self.data: dict = resolved_data # In case we miss anything and people can just do it themselves
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
    ... # Literally the same thing.

class Invite:
    def __init__(self, data: dict):
        self.code: str = data.get("code")
        self.guild: Optional[PartialGuild] = PartialGuild(
            data.get("guild")) if data.get("guild") else None
        self.channel: GuildChannel = GuildChannel(
            data.get("channel")) if data.get("channel") else None
        self.inviter: Optional[User] = User(
            data.get("inviter")) if data.get("inviter") else None
        self.target_type: int = data.get("target_type")
        self.target_user: Optional[User] = User(
            data.get("target_user")) if data.get("target_user") else None
        self.target_application: Optional[Application] = Application(
            data.get("target_application")) if data.get("target_application") else None
        self.approximate_presence_count: Optional[int] = data.get(
            "approximate_presence_count")
        self.approximate_member_count: Optional[int] = data.get(
            "approximate_member_count")
        self.expires_at: Optional[str] = data.get("expires_at")
        self.stage_instance: Optional[GuildStageChannel] = GuildStageChannel(
            data.get("stage_instance")) if data.get("stage_instance") else None
        self.guild_scheduled_event: Optional[GuildScheduledEvent] = GuildScheduledEvent(
            data.get("guild_scheduled_event"))


class GuildMember(User):
    def __init__(self, client, data: dict):
        super().__init__(client, data.get("user"))
        self.data = data
        self.client = client
        # self.user: Optional[User] = User(data["user"]) or None
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
            "communication_disabled_until")


class MentionedChannel:
    def __init__(self, data: dict):
        self.id: str = data.get("id")
        self.guild_id: str = data.get("guild_id")
        self.type: int = data.get("type")
        self.name: str = data.get("name")


class MentionedUser(User):
    def __init__(self, client, data: dict):
        super().__init__(client, data)
        self.member = GuildMember(client, data.get("member")) if data.get("member") else None

class MessageActivity:
    def __init__(self, data: dict):
        self.type: int = data.get("type")
        self.party_id: Optional[str] = data.get("party_id")


class AllowedMention:
    def __init__(self, allowed_mentions: List[str], replied_user: bool, roles: List[str], users: List[str]):
        self.data = {}
        self.data["parse"] = allowed_mentions
        self.data["replied_user"] = replied_user
        self.data["roles"] = roles
        self.data["users"] = users
        return self.data


class MessageInteraction:
    def __init__(self, client, data: dict):
        self.id: str = data.get("id")
        self.type: int = data.get("type")
        self.name: str = data.get("name")
        self.user: User = User(client, data.get("user"))
        self.member: Optional[GuildMember] = GuildMember(client, data.get("member")) if data.get("member") else None
        self.user: User = User(client, data.get("user"))



class SlashCommand(ApplicationCommand):
    def __init__(self, data: dict):
        super().__init__(data)
        self.options: Optional[List[AnyOption]] = data.get(
            "options")  # Return the type hinted class later this will take too long and is very tedious, I'll probably get Copilot to do it for me lmao
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

class SourceChannel:
    def __init__(self, data: dict):
        self.id: str = data.get("id")
        self.name: str = data.get("name")

class Webhook:  # Not used for making webhooks.
    def __init__(self, client, data: dict):
        self.id: str = data.get("id")
        self.client = client
        self.type: int = "Incoming" if data.get("type") == 1 else "Channel Follower" if data.get("type") == 2 else "Application"
        self.guild_id: Optional[str] = data.get("guild_id")
        self.channel_id: Optional[str] = data.get("channel_id")
        self.user: Optional[WebhookUser] = WebhookUser(data.get("user")) if data.get("user") else None
        self.name: Optional[str] = data.get("name")
        self.avatar: Optional[str] = data.get("avatar")
        self.token: str = data.get("token")
        self.application_id: Optional[str] = data.get("application_id")
        self.source_guild: Optional[PartialGuild] = PartialGuild(data.get("source_guild"))
        self.source_channel: Optional[SourceChannel] = SourceChannel(data.get("source_channel"))
        self.url: Optional[str] = data.get("url")

class Intents:
    def __init__(self, *, intents: Optional[int] = None):
        self.value = intents or 0

    @property
    def guilds(self):
        self.value += 1 << 0
        return self

    @property
    def guild_members(self):
        self.value += 1 << 1
        return self

    @property
    def guild_bans(self):
        self.value += 1 << 2
        return self

    @property
    def guild_emojis_and_stickers(self):
        self.value += 1 << 3
        return self

    @property
    def guild_integrations(self):
        self.value += 1 << 4
        return self

    @property
    def guild_webhooks(self):
        self.value += 1 << 5
        return self

    @property
    def guild_invites(self):
        self.value += 1 << 6
        return self

    @property
    def guild_voice_states(self):
        self.value += 1 << 7
        return self

    @property
    def guild_presences(self):
        self.value += 1 << 8
        return self

    @property
    def guild_messages(self):
        self.value += 1 << 9
        return self

    @property
    def guild_message_reactions(self):
        self.value += 1 << 10
        return self

    @property
    def guild_message_typing(self):
        self.value += 1 << 11
        return self

    @property
    def direct_messages(self):
        self.value += 1 << 12
        return self

    @property
    def direct_message_reactions(self):
        self.value += 1 << 13
        return self

    @property
    def direct_message_typing(self):
        self.value += 1 << 14
        return self

    @property
    def all(self):
        for attr in dir(self):
            if attr not in ["value", "all", "none", "remove_value", "add_intent"]:
                getattr(self, attr)
        return self

    @property
    def none(self):
        self.value = 0

    def remove_intent(self, intent: str) -> int:
        try:
            attr = getattr(self, intent.lower())
        except AttributeError:
            raise InvalidIntents(
                f"Intent {intent.lower()} is not a valid intent.")
        self.value -= attr.value
        return self.value

    def add_intent(self, intent: str) -> int:
        try:
            attr = getattr(self, intent)
        except AttributeError:
            raise InvalidIntents(f"Intent {intent} is not a valid intent.")
        self.value += attr
        return self.value

    @property
    def message_content(self):
        self.value += 1 << 15
        return self

    # TODO: Add some presets such as "Moderation", "Logging" etc.


class Permission:
    def __init__(self, *, bit: int = 0):
        self.value = bit

    @property
    def create_instant_invite(self):
        self.value += 1 << 0
        return self

    @property
    def kick_members(self):
        self.value += 1 << 1
        return self

    @property
    def ban_members(self):
        self.value += 1 << 2
        return self

    @property
    def administrator(self):
        self.value += 1 << 3
        return self

    @property
    def manage_channels(self):
        self.value += 1 << 4
        return self

    @property
    def manage_guild(self):
        self.value += 1 << 5
        return self

    @property
    def add_reactions(self):
        self.value += 1 << 6
        return self

    @property
    def view_audit_log(self):
        self.value += 1 << 7
        return self

    @property
    def priority_speaker(self):
        self.value += 1 << 8
        return self

    @property
    def stream(self):
        self.value += 1 << 9
        return self

    @property
    def read_messages(self):
        self.value += 1 << 10
        return self

    @property
    def send_messages(self):
        self.value += 1 << 11
        return self

    @property
    def send_tts_messages(self):
        self.value += 1 << 12
        return self

    @property
    def manage_messages(self):
        self.value += 1 << 13
        return self

    @property
    def embed_links(self):
        self.value += 1 << 14
        return self

    @property
    def attach_files(self):
        self.value += 1 << 15
        return self

    @property
    def read_message_history(self):
        self.value += 1 << 16
        return self

    @property
    def mention_everyone(self):
        self.value += 1 << 17
        return self

    @property
    def use_external_emojis(self):
        self.value += 1 << 18
        return self

    @property
    def connect(self):
        self.value += 1 << 20
        return self

    @property
    def speak(self):
        self.value += 1 << 21
        return self

    @property
    def mute_members(self):
        self.value += 1 << 22
        return self

    @property
    def deafen_members(self):
        self.value += 1 << 23
        return self

    @property
    def move_members(self):
        self.value += 1 << 24
        return self

    @property
    def use_voice_activation(self):
        self.value += 1 << 25
        return self

    @property
    def change_nickname(self):
        self.value += 1 << 26
        return self

    @property
    def manage_nicknames(self):
        self.value += 1 << 27
        return self

    @property
    def manage_roles(self):
        self.value += 1 << 28
        return self

    @property
    def manage_webhooks(self):
        self.value += 1 << 29
        return self

    @property
    def manage_emojis_and_stickers(self):
        self.value += 1 << 30
        return self

    @property
    def use_application_commands(self):
        self.value += 1 << 31
        return self

    @property
    def request_to_speak(self):
        self.value += 1 << 32
        return self

    @property
    def manage_events(self):
        self.value += 1 << 33
        return self

    @property
    def manage_threads(self):
        self.value += 1 << 34
        return self

    @property
    def create_public_threads(self):
        self.value += 1 << 35
        return self

    @property
    def create_private_threads(self):
        self.value += 1 << 36
        return self

    @property
    def use_external_stickers(self):
        self.value += 1 << 37
        return self

    @property
    def send_messages_in_threads(self):
        self.value += 1 << 38
        return self

    @property
    def start_embedded_activities(self):
        self.value += 1 << 39
        return self

    @property
    def moderator_members(self):
        self.value += 1 << 40
        return self

class VoiceState:
    def __init__(self, client, data: dict):
        self.data: dict = data
        self.guild_id: Optional[str] = data.get("guild_id")
        self.channel_id: str = data.get("channel_id")
        self.user_id: str = data.get("user_id")
        self.member: Optional[GuildMember] = GuildMember(client, data.get("member")) if data.get("member") else None
        self.session_id: str = data.get("session_id")
        self.deaf: bool = data.get("deaf")
        self.mute: bool = data.get("mute")
        self.self_deaf: bool = data.get("self_deaf")
        self.self_mute: bool = data.get("self_mute")
        self.self_stream: Optional[bool] = data.get("self_stream")
        self.self_video: bool = data.get("self_video")
        self.suppress: bool = data.get("suppress")
        self.request_to_speak_timestamp: datetime.datetime = datetime.datetime.fromisoformat(data.get("request_to_speak_timestamp"))

class Paginator:
    def __init__(self, *, pages: List[Embed]):
        self.current_index: int = 0
        self.pages = pages

    def back(self):
        return self.pages[self.current_index - 1]

    def forward(self):
        return self.pages[self.current_index + 1]

    def current(self):
        return self.pages[self.current_index]

    def add_page(self, page: Embed):
        self.pages.append(page)

    def remove_page(self, page: Embed):
        self.pages = len(filter(lambda embed: embed != page, self.pages))

    def current(self) -> Embed:
        return self.pages[self.current_index] 

class Shard(WebsocketClient):
    def __init__(self, token, intents, presence: Presence, shard_id, number_of_shards):
        super().__init__(token, intents, presence)
        self.shard_id = [shard_id, number_of_shards]

    async def identify(self):
        payload = {
            "op": self.IDENTIFY,
            "d": {
                "token": self.token,
                "intents": self.intents,
                "properties": {
                    "$os": platform,
                    "$browser": "EpikCord.py",
                    "$device": "EpikCord.py"
                },
                "shard": self.shard_id
            }
        }
        if self.presence:
            payload["d"]["presence"] = self.presence.to_dict()
        await self.send_json(payload)
    
    async def reconnect(self):
        await self.close()
        await self.connect()
        await self.identify()
        await self.resume()