import datetime
import io
import os
from logging import getLogger
from typing import Any, Dict, List, Optional, Union
from urllib.parse import quote as _quote

from .application import Application
from .colour import Colour
from .components import *
from .mentioned import MentionedChannel
from .partials import PartialEmoji
from .sticker import *
from .thread import Thread
from .type_enums import AllowedMentionTypes
from .user import User
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
        self.allowed_mentions: List[AllowedMentionTypes] = allowed_mentions
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
    def __init__(self, data: dict):
        self.type: int = data["type"]
        self.party_id: Optional[str] = data.get("party_id")


class Attachment:
    def __init__(self, data: dict):
        self.id: str = data["id"]
        self.file_name: str = data["filename"]
        self.description: Optional[str] = data.get("description")
        self.content_type: Optional[str] = data.get("content_type")
        self.size: int = data["size"]
        self.url: str = data["url"]
        self.proxy_url: str = data["proxy_url"]
        self.width: Optional[int] = data.get("width")
        self.height: Optional[int] = data.get("height")
        self.ephemeral: Optional[bool] = data.get("ephemeral")

    def to_dict(self) -> Dict[str, Any]:
        return _filter_values(
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
    count : int
        The amount of times this reaction has been added to the Message.
    me : bool
        If the ClientUser has reacted to this Message with this Reaction.
    emoji : PartialEmoji
        The partial emoji of this Reaction.
    """

    def __init__(self, data: dict):
        self.count: int = data["count"]
        self.me: bool = data.get["me"]  # type: ignore
        self.emoji: PartialEmoji = PartialEmoji(data["emoji"])


class Embed:
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
        self.type: Optional[int] = type
        self.title: Optional[str] = title
        self.description: Optional[str] = description
        self.url: Optional[str] = url
        self.video: Optional[dict] = video
        self.timestamp: Optional[datetime.datetime] = timestamp or None
        self.color: Optional[Colour] = color or colour
        self.footer: Optional[Dict] = footer
        self.image: Optional[Dict] = image
        self.thumbnail: Optional[Dict] = thumbnail
        self.provider: Optional[Dict] = provider
        self.author: Optional[Dict] = author
        self.fields: List[Dict] = fields or []

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
        config: Dict[str, Union[int, str]] = {"url": url}  # type: ignore
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
        config: Dict[str, Union[int, str]] = {"url": url}  # type: ignore
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
        config: Dict[str, Union[int, str]] = {"url": url}  # type: ignore
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
        from EpikCord import GuildMember, Reaction

        self.client = client
        self.id: int = int(data["id"])
        self.channel_id: int = int(data["channel_id"])
        self.channel = client.channels.get(self.channel_id)
        self.guild_id: Optional[str] = data.get("guild_id")
        self.webhook_id: Optional[str] = data.get("webhook_id")
        self.author: Optional[Union[WebhookUser, GuildMember, User]] = None

        if self.webhook_id:
            self.author = WebhookUser(data["author"])

        if data.get("member"):
            member_data = data["member"]
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
            Message(client, data["referenced_message"])
            if data.get("referenced_message")
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
        # * Cache it
        thread = Thread(self.client, await response.json())
        self.client.guilds[self.guild_id].channels[thread.id] = thread
        return Thread(self.client, await response.json())

    async def crosspost(self):
        response = await self.client.http.post(
            f"channels/{self.channel_id}/messages/{self.id}/crosspost"
        )
        return await response.json()


__all__ = (
    "AllowedMention",
    "MessageActivity",
    "Attachment",
    "Reaction",
    "Embed",
    "File",
    "Message",
)
