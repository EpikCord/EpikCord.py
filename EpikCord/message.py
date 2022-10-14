import asyncio
import datetime
import io
import os
from logging import getLogger
from typing import Any, Dict, List, Optional, TypedDict, Union
from urllib.parse import quote as _quote

import discord_typings
from typing_extensions import NotRequired

from .application import Application
from .colour import Colour
from .components import *
from .mentioned import MentionedChannel
from .partials import PartialEmoji
from .sticker import *
from .thread import Thread
from .type_enums import AllowedMentionTypes
from .user import User
from .utils import Utils
from .webhooks import WebhookUser

logger = getLogger(__name__)


def _filter_values(dictionary: dict) -> dict:
    return {k: v for k, v in dictionary.items() if v is not None}


class AllowedMention:
    def __init__(
        self,
        allowed_mentions: Union[List[AllowedMentionTypes], AllowedMentionTypes] = [],
        replied_user: bool = True,
        roles: List[int] = [],
        users: List[int] = [],
    ):
        self.allowed_mentions: Union[
            List[AllowedMentionTypes], AllowedMentionTypes
        ] = allowed_mentions
        self.replied_user: bool = replied_user
        self.roles: List[int] = roles
        self.users: List[int] = users

    def to_dict(self) -> Dict[str, Any]:
        return {
            "parse": self.allowed_mentions,
            "roles": self.roles,
            "users": self.users,
            "replied_user": self.replied_user,
        }


class MessageActivity:
    def __init__(self, data: discord_typings.MessageActivityData):
        self.type: int = data["type"]
        self.party_id: Optional[str] = data.get("party_id")


class Attachment:
    def __init__(self, data: discord_typings.AttachmentData):
        self.id: int = int(data["id"])
        self.file_name: str = data["filename"]
        self.description: Optional[str] = data.get("description")
        self.content_type: Optional[str] = data.get("content_type")
        self.size: int = data["size"]
        self.url: str = data["url"]
        self.proxy_url: str = data["proxy_url"]
        self.width: Optional[int] = data.get("width")
        self.height: Optional[int] = data.get("height")
        self.ephemeral: Optional[bool] = data.get("ephemeral")

    def to_dict(self) -> discord_typings.AttachmentData:
        return _filter_values(  # type: ignore
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


class Reaction:
    """
    A class representation of a Reaction.
    Not for direct use.


    Attributes
    ----------
    count: int
        The amount of times this reaction has been added to the Message.
    me: bool
        If the ClientUser has reacted to this Message with this Reaction.
    emoji: PartialEmoji
        The partial emoji of this Reaction.
    """

    def __init__(self, data: discord_typings.MessageReactionData):
        self.count: int = data["count"]
        self.me: bool = data.get["me"]  # type: ignore
        self.emoji: PartialEmoji = PartialEmoji(data["emoji"])


class Embed:
    def __init__(
        self,
        *,
        title: Optional[str] = None,
        description: Optional[str] = None,
        color: Optional[Union[Colour, int]] = None,
        colour: Optional[Union[Colour, int]] = None,
        video: Optional[discord_typings.EmbedVideoData] = None,
        timestamp: Optional[datetime.datetime] = None,
        url: Optional[str] = None,
        footer: Optional[discord_typings.EmbedFooterData] = None,
        image: Optional[discord_typings.EmbedImageData] = None,
        thumbnail: Optional[discord_typings.EmbedThumbnailData] = None,
        provider: Optional[discord_typings.EmbedProviderData] = None,
        author: Optional[discord_typings.EmbedAuthorData] = None,
        fields: List[discord_typings.EmbedFieldData] = [],
    ):
        self.title: Optional[str] = title
        self.description: Optional[str] = description
        self.url: Optional[str] = url
        self.video: Optional[discord_typings.EmbedVideoData] = video
        self.timestamp: Optional[datetime.datetime] = timestamp or None
        self.color: Optional[Colour] = color or colour  # type: ignore
        self.footer: Optional[discord_typings.EmbedFooterData] = footer
        self.image: Optional[discord_typings.EmbedImageData] = image
        self.thumbnail: Optional[discord_typings.EmbedThumbnailData] = thumbnail
        self.provider: Optional[discord_typings.EmbedProviderData] = provider
        self.author: Optional[discord_typings.EmbedAuthorData] = author
        self.fields: List[discord_typings.EmbedFieldData] = fields

    def add_field(self, *, name: str, value: str, inline: bool = False):
        self.fields.append({"name": name, "value": value, "inline": inline})

    def set_thumbnail(
        self,
        *,
        url: str,
        proxy_url: Optional[str] = None,
        height: Optional[int] = None,
        width: Optional[int] = None,
    ):
        config: discord_typings.EmbedThumbnailData = {"url": url}
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
        url: str,
        proxy_url: Optional[str] = None,
        height: Optional[int] = None,
        width: Optional[int] = None,
    ):
        config: discord_typings.EmbedVideoData = {"url": url}
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
        url: str,
        proxy_url: Optional[str] = None,
        height: Optional[int] = None,
        width: Optional[int] = None,
    ):
        config: discord_typings.EmbedImageData = {"url": url}
        if proxy_url:
            config["proxy_url"] = proxy_url
        if height:
            config["height"] = height
        if width:
            config["width"] = width

        self.image = config

    def set_provider(self, *, name: Optional[str] = None, url: Optional[str] = None):
        config: discord_typings.EmbedProviderData = {}
        if name:
            config["name"] = name
        if url:
            config["url"] = url
        self.provider = config

    def set_footer(
        self,
        *,
        text: str,
        icon_url: Optional[str] = None,
        proxy_icon_url: Optional[str] = None,
    ):
        payload: discord_typings.EmbedFooterData = {
            "text": text,
        }
        if icon_url:
            payload["icon_url"] = icon_url
        if proxy_icon_url:
            payload["proxy_icon_url"] = proxy_icon_url
        self.footer = payload

    def set_author(
        self,
        name: str,
        url: Optional[str] = None,
        icon_url: Optional[str] = None,
        proxy_icon_url: Optional[str] = None,
    ):
        payload: discord_typings.EmbedAuthorData = {"name": name}
        if url:
            payload["url"] = url
        if icon_url:
            payload["icon_url"] = icon_url
        if proxy_icon_url:
            payload["proxy_icon_url"] = proxy_icon_url

        self.author = payload

    def set_fields(self, *, fields: List[discord_typings.EmbedFieldData]):
        for field in fields:

            if not field["name"] or not field["value"]:
                raise ValueError("Field name and value are required")

        self.fields = fields

    def set_color(self, *, colour: Colour):
        self.color = colour

    def set_timestamp(self, *, timestamp: Optional[datetime.datetime] = None):
        self.timestamp = timestamp or None

    def set_title(self, title: Optional[str] = None):
        self.title = title

    def set_description(self, description: Optional[str] = None):
        self.description = description

    def set_url(self, url: Optional[str] = None):
        self.url = url

    def to_dict(self):
        return {
            key: value
            for key, value in self.__dict__.items()
            if value is not None or key.startswith("_")
        }

    @classmethod
    def from_dict(cls, data: discord_typings.EmbedData):
        payload = data
        payload.pop("type", None)
        payload["timestamp"] = datetime.datetime.fromisoformat(data["timestamp"])  # type: ignore
        return cls(**payload)  # type: ignore


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
        self.fp.close = lambda: None  # type: ignore

        if filename is None:
            if isinstance(fp, str):
                _, self.filename = os.path.split(fp)
            else:
                self.filename = getattr(fp, "name", None)  # type: ignore
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
        self.fp.close = self._closer  # type: ignore
        self._closer()


class MessageReference:
    def __init__(self, data: discord_typings.MessageReferenceData) -> None:
        self.message_id: Optional[int] = (
            int(data["message_id"]) if data.get("message_id") else None
        )
        self.channel_id: Optional[int] = (
            int(data["channel_id"]) if data.get("channel_id") else None
        )
        self.guild_id: Optional[int] = (
            int(data["guild_id"]) if data.get("guild_id") else None
        )
        self.fail_if_not_exists: Optional[bool] = data.get("fail_if_not_exists")


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

    def __init__(self, client, data: discord_typings.MessageData):
        from EpikCord import GuildMember, Reaction

        self.client = client
        self.id: int = int(data["id"])
        self.channel_id: int = int(data["channel_id"])
        self.guild_id: Optional[int] = int(data["guild_id"]) if data.get("guild_id") else None  # type: ignore
        self.webhook_id: Optional[int] = (
            int(data["webhook_id"]) if data.get("webhook_id") else None
        )
        self.author: Optional[Union[WebhookUser, GuildMember, User]] = None

        if self.webhook_id:
            self.author = WebhookUser(data["author"])

        if data.get("member"):
            member_data = data["member"]  # type: ignore
            if data.get("author"):
                member_data["user"] = data["author"]
            self.author = GuildMember(self, member_data)
        else:
            self.author = User(self, data["author"]) if data.get("author") else None

        self.content: Optional[str] = data.get("content")
        self.timestamp: datetime.datetime = datetime.datetime.fromisoformat(
            data["timestamp"]
        )
        self.edited_timestamp: Optional[str] = (
            datetime.datetime.fromisoformat(data["edited_timestamp"])  # type: ignore
            if data.get("edited_timestamp")
            else None
        )
        self.tts: bool = data["tts"]
        self.mention_everyone: bool = data["mention_everyone"]
        self.mentions: Optional[List[User]] = [
            User(client, user) for user in data.get("mentions", [])
        ]
        self.mention_roles: Optional[List[int]] = (
            [int(r) for r in data["mention_roles"]]
            if data.get("mention_roles")
            else None
        )
        self.mention_channels: Optional[List[MentionedChannel]] = [
            MentionedChannel(channel) for channel in data.get("mention_channels", [])
        ]
        self.embeds: Optional[List[Embed]] = [
            Embed.from_dict(embed) for embed in data.get("embeds", [])
        ]
        self.reactions: Optional[List[Reaction]] = [
            Reaction(reaction) for reaction in data.get("reactions", [])
        ]
        self.nonce: Optional[Union[int, str]] = data.get("nonce")
        self.pinned: bool = data["pinned"]
        self.type: int = data["type"]
        self.activity: Optional[MessageActivity] = (
            MessageActivity(data["activity"]) if data.get("activity") else None
        )
        # * Despite there being a PartialApplication,
        # * Discord don't specify what attributes it has
        self.application: Optional[Application] = (
            Application(data["application"]) if data.get("application") else None
        )
        self.flags: Optional[int] = data.get("flags")
        self.referenced_message: Optional[Message] = (
            Message(client, data["referenced_message"])  # type: ignore # MyPy being dumb
            if data.get("referenced_message")
            else None
        )
        self.message_reference: Optional[MessageReference] = (
            MessageReference(data["message_reference"])
            if data.get("message_reference")
            else None
        )
        from .interactions import MessageInteraction

        self.interaction: Optional[MessageInteraction] = (
            MessageInteraction(client, data["interaction"])
            if data.get("interaction")
            else None
        )
        self.thread: Optional[Thread] = (
            Thread(self.client, data["thread"]) if data.get("thread") else None
        )
        self.components: Optional[List[Union[TextInput, SelectMenu, Button]]] = (
            [ActionRow.from_dict(component) for component in data["components"]]
            if data.get("components")
            else None
        )

        self.sticker_items: Optional[List[StickerItem]] = [
            StickerItem(sticker) for sticker in data["sticker_items"]
        ] if data.get("sticker_items") else None

        self.channel = client.channels.get(self.channel_id)
        if not self.channel:  # Cache miss
            self.channel = asyncio.create_task(client.channels.fetch(self.channel_id))

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

    async def delete(self, reason: str):
        headers = self.client.headers.copy()
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        response = await self.client.http.delete(
            f"channels/{self.channel_id}/messages/{self.id}", headers=headers
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
        auto_archive_duration: Optional[int] = None,
        rate_limit_per_user: Optional[int] = None,
    ):
        payload = Utils.filter_values(
            {
                "name": name,
                "auto_archive_duration": auto_archive_duration,
                "rate_limit_per_user": rate_limit_per_user,
            }
        )

        response = await self.client.http.post(
            f"channels/{self.channel_id}/messages/{self.id}/threads",
            json=payload,
        )
        # * Cache it
        thread = Thread(self.client, await response.json())
        self.client.guilds[self.guild_id].channels[thread.id] = thread
        return Thread(self.client, await response.json())

    async def crosspost(self):
        response = await self.client.http.post(
            f"channels/{self.channel_id}/messages/{self.id}/crosspost"
        )
        return await response.json()


class MessagePayload(TypedDict):
    content: NotRequired[str]
    nonce: NotRequired[Union[int, str]]
    tts: NotRequired[bool]
    embeds: NotRequired[List[discord_typings.EmbedData]]
    allowed_mentions: NotRequired[discord_typings.AllowedMentionsData]
    message_reference: NotRequired[discord_typings.MessageReferenceData]
    components: NotRequired[List[discord_typings.ActionRowData]]
    sticker_ids: NotRequired[List[int]]
    attachments: NotRequired[List[discord_typings.AttachmentData]]
    flags: NotRequired[int]


__all__ = (
    "AllowedMention",
    "MessageActivity",
    "Attachment",
    "Reaction",
    "Embed",
    "File",
    "Message",
    "MessagePayload",
    "MessageReference",
)
