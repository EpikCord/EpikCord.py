import os
import io
import datetime
from .colour import Colour
from logging import getLogger
from .thread import Thread
from typing import Union, Optional, List
from urllib.parse import quote as _quote
from .sticker import *
from .application import Application
from .components import *

logger = getLogger(__name__)


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
        self.type: int = type
        self.title: Optional[str] = title
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
        for key, value in self.__dict__.items():
            if value is None and not key.startswith("_"):
                continue
            final_product[key] = value
        return final_product


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
        from EpikCord import (
            WebhookUser,
            GuildMember,
            User,
            MentionedChannel,
            Reaction,
            MessageActivity,
            MessageInteraction,
        )

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
        # * Despite there being a PartialApplication,
        # * Discord don't specify what attributes it has
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
        # * Cache it
        self.client.guilds[self.guild_id].append(Thread(await response.json()))
        return Thread(await response.json())

    async def crosspost(self):
        response = await self.client.http.post(
            f"channels/{self.channel_id}/messages/{self.id}/crosspost"
        )
        return await response.json()
