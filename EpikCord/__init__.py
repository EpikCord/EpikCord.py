import threading
from .managers import *
from threading import Event
from aiohttp import *
import asyncio 
from base64 import b64encode
import datetime
import re
from logging import getLogger
from typing import *
from urllib.parse import quote

CT = TypeVar('CT', bound='Colour')
T = TypeVar('T')
logger = getLogger(__name__)


"""
Some parts of the code is done by discord.py and their amazing team of contributors
The MIT License (MIT)
Copyright © 2015-2021 Rapptz
Copyright © 2021-present EpikHost
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE."""


_MARKDOWN_ESCAPE_SUBREGEX = '|'.join(r'\{0}(?=([\s\S]*((?<!\{0})\{0})))'.format(c) for c in ('*', '`', '_', '~', '|'))

_MARKDOWN_ESCAPE_COMMON = r'^>(?:>>)?\s|\[.+\]\(.+\)'

_MARKDOWN_ESCAPE_REGEX = re.compile(fr'(?P<markdown>{_MARKDOWN_ESCAPE_SUBREGEX}|{_MARKDOWN_ESCAPE_COMMON})', re.MULTILINE)

_URL_REGEX = r'(?P<url><[^: >]+:\/[^ >]+>|(?:https?|steam):\/\/[^\s<]+[^<.,:;\"\'\]\s])'

_MARKDOWN_STOCK_REGEX = fr'(?P<markdown>[_\\~|\*`]|{_MARKDOWN_ESCAPE_COMMON})'


def _cancel_tasks(loop) -> None:
    tasks = {t for t in asyncio.all_tasks(loop=loop) if not t.done()}

    if not tasks:
        return

    for task in tasks:
        task.cancel()
    logger.debug(f"Cancelled {len(tasks)} tasks")
    loop.run_until_complete(asyncio.gather(*tasks, return_exceptions=True))

def _cleanup_loop(loop) -> None:
    try:
        _cancel_tasks(loop)
        logger.debug("Shutting down async generators.")
        loop.run_until_complete(loop.shutdown_asyncgens())
    finally:
        loop.close()
    
    
class UnavailableGuild:
    def __init__(self, data):
        self.data = data
        self.id: str = data["id"]
        self.available: bool = data["available"]

class PartialEmoji:
    def __init__(self, data):
        self.data: dict = data
        self.name: str = data["name"]
        self.id: str = data["id"]
        self.animated: bool = data["animated"]
    
class Reaction:
    def __init__(self, data: dict):
        self.count: int = data["count"]
        self.me: bool = data["me"]
        self.emoji: PartialEmoji = PartialEmoji(data["emoji"])

class Message:
    def __init__(self, client, data: dict):
        self.client = client
        self.id: str = data["id"]
        self.channel_id: str = data["channel_id"]
        self.guild_id: Optional[str] = data["guild_id"] or None
        self.webhook_id: Optional[str] = data["webhook_id"] or None
        self.author: Optional[User] if not self.webhook_id else WebhookUser = WebhookUser(data["author"]) if self.webhook_id else User(data["author"])
        self.member: Optional[GuildMember] = GuildMember(data["member"]) if data["member"] else None
        self.content: Optional[str] = data["content"] or None # I forgot Message Intents are gonna stop this.
        self.timestamp: str = data["timestamp"]
        self.edited_timestamp: Optional[str] = data["edited_timestamp"] or None
        self.tts: bool = data["tts"]
        self.mention_everyone: bool = data["mention_everyone"]
        self.mentions: Optional[List[MentionedUser]] = [MentionedUser(mention) for mention in data["mentions"]] or None
        self.mention_roles: Optional[List[int]] = data["mention_roles"] or None
        self.mention_channels: Optional[List[MentionedChannel]] = [MentionedChannel(channel) for channel in data["mention_channels"]] or None
        self.embeds: Optional[List[Embed]] = [Embed(embed) for embed in data["embeds"]] or None
        self.reactions: Optional[List[Reaction]] = [Reaction(reaction) for reaction in data["reactions"]] or None
        self.nonce: Optional[Union[int, str]] = data["nonce"] or None
        self.pinned: bool = data["pinned"]
        self.type: int = data["type"]
        self.activity: MessageActivity = MessageActivity(data["activity"])
        self.application: Application = Application(data["application"]) # Despite there being a PartialApplication, Discord don't specify what attributes it has
        self.flags: int = data["flags"]
        self.referenced_message: Optional[Message] = Message(data["referenced_message"]) if data["referenced_message"] else None
        self.interaction: Optional[MessageInteraction] = MessageInteraction(client, data["interaction"]) if data["interaction"] else None
        self.thread: Thread = Thread(data["thread"]) if data["thread"] else None
        self.components: Optional[List[Union[MessageSelectMenu, MessageButton]]] = [MessageSelectMenu(component) if component["type"] == 1 else MessageButton(component) for component in data["components"]] or None
        self.stickers: Optional[List[StickerItem]] = [StickerItem(sticker) for sticker in data["stickers"]] or None
        
    async def add_reaction(self, emoji: str):
        emoji = quote(emoji)
        logger.debug(f"Added a reaction to message ({self.id}).")
        response = await self.client.http.put(f"channels/{self.channel_id}/messages/{self.id}/reactions/{emoji}/@me")
        return await response.json()
    
    async def remove_reaction(self, emoji: str, user = None):
        emoji = quote(emoji)
        logger.debug(f"Removed reaction {emoji} from message ({self.id}) for user {user.username}.")
        if not user:
            response = await self.client.http.delete(f"channels/{self.channel_id}/messages/{self.id}/reactions/{emoji}/@me")
        else:
            response = await self.client.http.delete(f"channels/{self.channel_id}/messages/{self.id}/reactions/{emoji}/{user.id}")
        return await response.json()
    
    async def fetch_reactions(self,*, after, limit) -> List[Reaction]:
        logger.debug(f"Fetching reactions from message ({self.id}).")
        response = await self.client.http.get(f"channels/{self.channel_id}/messages/{self.id}/reactions?after={after}&limit={limit}")
        return await response.json()
    
    async def delete_all_reactions(self):
        logger.debug(f"Deleting all reactions from message ({self.id}).")
        response = await self.client.http.delete(f"channels/{self.channel_id}/messages/{self.id}/reactions")
        return await response.json()
    
    async def delete_reaction_for_emoji(self, emoji: str):
        logger.debug(f"Deleting a reaction from message ({self.id}) for emoji {emoji}.")
        emoji = quote(emoji)
        response = await self.client.http.delete(f"channels/{self.channel_id}/messages/{self.id}/reactions/{emoji}")
        return await response.json()
    
    async def edit(self, message_data: dict):
        logger.debug(f"Editing message {self.id} with message_data {message_data}.")
        response = await self.client.http.patch(f"channels/{self.channel_id}/messages/{self.id}", data=message_data)
        return await response.json()
    
    async def delete(self):
        logger.debug(f"Deleting message {self.id}.")
        response = await self.client.http.delete(f"channels/{self.channel_id}/messages/{self.id}")
        return await response.json()
    
    async def pin(self, *, reason: Optional[str]):
        headers = self.client.http.headers.copy()
        if reason:
            headers["X-Audit-Log-Reason"] = reason
            logger.debug(f"Pinning message {self.id} with reason {reason}.")
        else:
            logger.debug(f"Pinning message {self.id}.")
        response = await self.client.http.put(f"channels/{self.channel_id}/pins/{self.id}", headers=headers)
        return await response.json()
    
    async def unpin(self, *, reason: Optional[str]):
        headers = self.client.http.headers.copy()
        if reason:
            headers["X-Audit-Log-Reason"] = reason
            logger.debug(f"Unpinning message {self.id} with reason {reason}.")
        else:
            logger.debug(f"Unpinning message {self.id}.")
        response = await self.client.http.delete(f"channels/{self.channel_id}/pins/{self.id}", headers=headers)
        return await response.json()

    async def start_thread(self, name: str, auto_archive_duration: Optional[int], rate_limit_per_user: Optional[int]):
        logger.debug(f"Starting thread for message {self.id} with name {name}, auto archive duration {auto_archive_duration or None}, ratelimit per user {rate_limit_per_user or None}.")
        response = await self.client.http.post(f"channels/{self.channel_id}/messages/{self.id}/threads", data={"name": name, "auto_archive_duration": auto_archive_duration, "rate_limit_per_user": rate_limit_per_user})
        self.client.guilds[self.guild_id].append(Thread(await response.json())) # Cache it
        return Thread(await response.json())
    
    async def crosspost(self):
        logger.debug(f"Crossposting message {self.id}.")
        response = await self.client.http.post(f"channels/{self.channel_id}/messages/{self.id}/crosspost")
        return await response.json()
        
class Messageable:
    def __init__(self, client, channel_id: str):
        self.channel_id: str = channel_id
        self.client = client
        
    async def fetch_messages(self,*, around: Optional[str] = None, before: Optional[str] = None, after: Optional[str] = None, limit: Optional[int] = None) -> List[Message]:
        response = await self.client.http.get(f"channels/{self.id}/messages", params={"around": around, "before": before, "after": after, "limit": limit})
        data = await response.json()
        return [Message(message) for message in data]
    
    async def fetch_message(self,*, message_id: str) -> Message:
        response = await self.client.http.get(f"channels/{self.id}/messages/{message_id}")
        data = await response.json()
        return Message(data)

    async def send(self, message_data: dict) -> Message:
        response = await self.client.http.post(f"channels/{self.id}/messages", form=message_data)
        return Message(await response.json())

class User(Messageable):
    def __init__(self, client, data: dict):
        self.data = data
        self.client = client
        self.id: str = data["id"]
        self.username: str = data["username"]
        self.discriminator: str = data["discriminator"]
        self.avatar: Optional[str] = data["avatar"]
        self.bot: bool = data["bot"]
        self.system: Optional[bool] = data["system"]
        self.mfa_enabled: bool = data["mfa_enabled"]
        self.banner: Optional[str] = data["banner"] or None
        self.accent_color: Optional[int] = data["accent_color"] or None # the user's banner color encoded as an integer representation of hexadecimal color code	
        self.locale: Optional[str] = data["locale"] or None
        self.verified: bool = data["verified"]
        self.email: Optional[str] = data["email"] or None
        self.flags: int = data["flags"]
        self.premium_type: int = data["premium_type"]
        self.public_flags: int = data["public_flags"]

class EventHandler:
    # Class that'll contain all methods that'll be called when an event is triggered.    

    def __init__(self):
        self.events = {}

    async def handle_events(self):
        async for event in self.ws:
            event = event.json()

            if event["op"] == self.HELLO:

                self.interval = event["d"]["heartbeat_interval"]

                await self.identify()

            elif event["op"] == self.EVENT:
                await self.handle_event(event["t"], event["d"])

            elif event["op"] == self.HEARTBEAT:
                await self.heartbeat(True) # I shouldn't wait the remaining delay according to the docs.

            elif event["op"] == self.HEARTBEAT_ACK:
                try:
                    self.heartbeats.append(event["d"])
                except AttributeError:
                    self.heartbeats = [event["d"]]
                self.sequence = event["s"]
            logger.debug(f"Received event {event['t']}")

    async def handle_event(self, event_name: str, data: dict):
        event_name = event_name.lower()
        try:
            await getattr(self, event_name)(data)
        except AttributeError:
            logger.warning(f"A new event, {event_name}, has been added and EpikCord hasn't added that yet. Open an issue to be the first!")

    async def message_create(self, data: dict):
        await self.events["message_create"](Message(self.client, data))

    def event(self, func):
        self.events[func.__name__.lower().replace("on_", "")] = func

    async def ready(self, data: dict):
        self.user: ClientUser = ClientUser(self.session, data["user"])
        self.application: Application = await self.session.get("https://discord.com/api/v9/oauth2/applications/@me", headers={"Authorization": f"Bot {self.token}"})

        def heartbeater():
            loop = asyncio.new_event_loop()
            loop.run_until_complete(self.heartbeat(False))

        thread = threading._start_new_thread(heartbeater, ())
        await self.events["ready"]()

    

class WebsocketClient(EventHandler):
    def __init__(self, token: str, intents: int):

        super().__init__()

        self.EVENT = 0
        self.HEARTBEAT = 1
        self.IDENTIFY = 2
        self.PRESENCE_UPDATE = 3
        self.VOICE_STATE_UPDATE = 4
        self.RESUME = 6
        self.RECONNECT = 7
        self.REQUEST_GUILD_MEMBERS = 8
        self.INVALID_SESSION = 9
        self.HELLO = 10
        self.HEARTBEAT_ACK = 11

        self.token = token
        self.heartbeat_event = Event
        self.intents = intents
        self.loop = asyncio.new_event_loop()
        self.session = ClientSession()
        self.commands = {}
        self._closed = True # Well nah we're starting closed
        self.hearbeats = []
        self.average_latency = 0

        self.interval = None # How frequently to heartbeat
        self.session_id = None
        self.sequence = None

    async def heartbeat(self, forced: Optional[bool] = None):
        if forced:
            return await self.send_json({"op": self.HEARTBEAT, "d": self.sequence or "null"})

        if self.interval:
            while True:
                await asyncio.sleep(self.interval / 1000)
                await self.send_json({"op": self.HEARTBEAT, "d": self.sequence or "null"})
                logger.debug("Sent a heartbeat!")
        
    async def send_json(self, json: dict):
        try:
            await self.ws.send_json(json)
        except:
            logger.debug(f"Exited with code: {self.ws.close_code}")

    async def connect(self):
        self.ws = await self.session.ws_connect("wss://gateway.discord.gg/?v=9&encoding=json")
        await self.handle_events()
        self._closed = False

    async def resume(self):
        await self.send_json({
            'op': self.RESUME,
            'd': {
                'seq': self.sequence,
                'session_id': self.session_id,
                'token': self.token
            }
        })
        self._closed = False

    async def identify(self):
        await self.send_json({
            "op": self.IDENTIFY,
            "d": {
                "token": self.token,
                "intents": self.intents,
                "properties": {
                    "$os": "linux",
                    "$browser": "EpikCord.py",
                    "$device": "EpikCord.py"
                    }
                }
            }
        )

    async def close(self) -> None:
        if self._closed:
            return

        self._closed = True

        # for voice in self.voice_clients:
        #     try:
        #         await voice.disconnect(force=True)
        #     except Exception:
        #         # if an error happens during disconnects, disregard it.
        #         pass

        if self.ws is not None:
            if not self.ws.closed:
                await self.ws.close(code=1000)

        if self.http is not None:
            if not self.http.closed:
                await self.http.close()

        self._closed = True

    def login(self):

        loop = asyncio.get_event_loop()

        async def runner():
            try:
                await self.connect()
            finally:
                if self._closed != True:
                    await self.close()

        def stop_loop_on_completion(f: asyncio.Future):
            loop.stop()

        future = asyncio.ensure_future(runner(), loop=loop)
        future.add_done_callback(stop_loop_on_completion)
        
        try:
            loop.run_forever()
        except KeyboardInterrupt:
            ...
        finally:
            future.remove_done_callback(stop_loop_on_completion)
            _cleanup_loop(loop)
            
class BaseSlashCommandOption:
    def __init__(self, *, name: str, description: str, required: bool = False):
        self.settings = {
            "name": name,
            "description": description,
            "required": required
        }
        # People shouldn't use this class, this is just a base class for other options

class Subcommand(BaseSlashCommandOption):
    def __init__(self, *, name: str, description: Optional[str] = None, required: bool = False):
        super().__init__(name=name, description=description, required=required)
        self.settings["type"] = 1
        
class SubCommandGroup(BaseSlashCommandOption):
    def __init__(self, *, name: str, description: Optional[str] = None, required: bool = False):
        super().__init__(name=name, description=description, required=required)
        self.settings["type"] = 2
        
class StringOption(BaseSlashCommandOption):
    def __init__(self, *, name: str, description: Optional[str] = None, required: bool = False):
        super().__init__(name=name, description=description, required=required)
        self.settings["type"] = 3
        
class IntegerOption(BaseSlashCommandOption):
    def __init__(self, *, name: str, description: Optional[str] = None, required: bool = False):
        super().__init__(name=name, description=description, required=required)
        self.settings["type"] = 4
        
class BooleanOption(BaseSlashCommandOption):
    def __init__(self, *, name: str, description: Optional[str] = None, required: bool = False):
        super().__init__(name=name, description=description, required=required)
        self.settings["type"] = 5
        
class UserOption(BaseSlashCommandOption):
    def __init__(self, *, name: str, description: Optional[str] = None, required: bool = False):
        super().__init__(name=name, description=description, required=required)
        self.settings["type"] = 6
        
class ChannelOption(BaseSlashCommandOption):
    def __init__(self, *, name: str, description: Optional[str] = None, required: bool = False):
        super().__init__(name=name, description=description, required=required)
        self.settings["type"] = 7
        
class RoleOption(BaseSlashCommandOption):
    def __init__(self, *, name: str, description: Optional[str] = None, required: bool = False):
        super().__init__(name=name, description=description, required=required)
        self.settings["type"] = 8

class MentionableOption(BaseSlashCommandOption):
    def __init__(self, *, name: str, description: Optional[str] = None, required: bool = False):
        super().__init__(name=name, description=description, required=required)
        self.settings["type"] = 9
    
class NumberOption(BaseSlashCommandOption):
    def __init__(self, *, name: str, description: Optional[str] = None, required: bool = False):
        super().__init__(name=name, description=description, required=required)
        self.settings["type"] = 10

class SlashCommandOptionChoice:
    def __init__(self, * name: str, value: Union[float, int, str]):
        self.settings = {
            "name": name,
            "value": value
        }

class Overwrite:
    def __init__(self, data: dict):
        self.id: str = data["id"]
        self.type: int = data["type"]
        self.allow: str = data["allow"]
        self.deny: str = data["deny"]


class StickerItem:
    def __init__(self, data: dict):
        self.id: str = data["id"]
        self.name: str = data["name"]
        self.description: str = data["description"]
        self.tags: str = data["tags"]
        self.type: str = data["image"]
        self.format_type: int = data["format_type"]
        self.pack_id: int = data["pack_id"]
        self.sort_value: int = data["sort_value"]

class ThreadMember:
    def __init__(self, data: dict):
        self.id: str = data["user_id"]
        self.thread_id: str = data["thread_id"]
        self.join_timestamp: str = data["join_timestamp"]
        self.flags: int = data["flags"]

class Thread:
    def __init__(self, client, data: dict):
        super().__init__(client, data)
        self.owner_id: str = data["owner_id"]
        self.message_count: int = data["message_count"]
        self.member_count: int = data["member_count"]
        self.archived: bool = data["archived"]
        self.auto_archive_duration: int = data["auto_archive_duration"]
        self.archive_timestamp: str = data["archive_timestamp"]
        self.locked: bool = data["locked"]
    
    async def join(self):
        if self.archived:
            raise ThreadArchived("This thread has been archived so it is no longer joinable")
        response = await self.client.http.put(f"/channels/{self.id}/thread-members/@me")
        return await response.json()
    
    async def add_member(self, member_id: str):
        if self.archived:
            raise ThreadArchived("This thread has been archived so it is no longer joinable")
        
        response = await self.client.http.put(f"/channels/{self.id}/thread-members/{member_id}")
        return await response.json()
    
    async def leave(self):
        if self.archived:
            raise ThreadArchived("This thread has been archived so it is no longer leaveable")
        response = await self.client.http.delete(f"/channels/{self.id}/thread-members/@me")
        return await response.json()
    
    async def remove_member(self, member_id: str):
        if self.archived:
            raise ThreadArchived("This thread has been archived so it is no longer leaveable")
        
        response = await self.client.http.delete(f"/channels/{self.id}/thread-members/{member_id}")
        return await response.json()
    
    async def fetch_member(self, member_id: str) -> ThreadMember:
        response = await self.client.http.get(f"/channels/{self.id}/thread-members/{member_id}")
        if response.status == 404:
            raise NotFound404("The member you are trying to fetch does not exist")
        return ThreadMember(await response.json())
    
    async def list_members(self) -> List[ThreadMember]:
        response = await self.client.http.get(f"/channels/{self.id}/thread-members")
        return [ThreadMember(member) for member in await response.json()]

    async def bulk_delete(self, message_ids: List[str], reason: Optional[str]) -> None:

        if reason:
            headers = self.client.http.headers.copy()
            headers["X-Audit-Log-Reason"] = reason
            
        response = await self.client.http.post(f"channels/{self.id}/messages/bulk-delete", data={"messages": message_ids}, headers=headers)
        return await response.json()

def _get_mime_type_for_image(data: bytes):
    if data.startswith(b'\x89\x50\x4E\x47\x0D\x0A\x1A\x0A'):
        return 'image/png'
    elif data[0:3] == b'\xff\xd8\xff' or data[6:10] in (b'JFIF', b'Exif'):
        return 'image/jpeg'
    elif data.startswith((b'\x47\x49\x46\x38\x37\x61', b'\x47\x49\x46\x38\x39\x61')):
        return 'image/gif'
    elif data.startswith(b'RIFF') and data[8:12] == b'WEBP':
        return 'image/webp'
    else:
        raise InvalidArgumentType('Unsupported image type given')


def _bytes_to_base64_data(data: bytes) -> str:
    fmt = 'data:{mime};base64,{data}'
    mime = _get_mime_type_for_image(data)
    b64 = b64encode(data).decode('ascii')
    return fmt.format(mime=mime, data=b64)

class BaseChannel:
    def __init__(self, client, data: dict):
        self.id: str = data["id"]
        self.client = client
        self.type = data["type"]


class BaseComponent:
    def __init__(self):
        self.settings = {}

    def set_custom_id(self, custom_id: str):
        
        if not isinstance(custom_id, str):
            raise InvalidArgumentType("Custom Id must be a string.")
        
        elif len(custom_id) > 100:
            raise CustomIdIsTooBig("Custom Id must be 100 characters or less.")

        self.settings["custom_id"] = custom_id
class Application:
    def __init__(self, client, data: dict):
        self.id: str = data["id"]
        self.client = client
        self.name: str = data["name"]
        self.icon: Optional[str] = data["icon"] or None
        self.description: str = data["description"]
        self.rpc_origins: Optional[list] = data["rpc_origins"] or None
        self.bot_public: bool = data["bot_public"]
        self.bot_require_code_grant: bool = data["bot_require_code_grant"]
        self.terms_of_service_url: Optional[str] = data["terms_of_service"] or None
        self.privacy_policy_url: Optional[str] = data["privacy_policy"] or None
        self.owner: PartialUser = PartialUser(data["user"])
        self.summary: str = data["summary"]
        self.verify_key: str = data["verify_key"]
        self.team: Optional[Team] = Team(data["team"]) or None
        self.cover_image: Optional[str] = data["cover_image"] or None
        self.flags: int = data["flags"]

    async def fetch(self):
        response: ClientResponse = await self.client.http.get("oauth2/applications/@me")
        data: dict = await response.json()
        self.application = Application(data)

class ApplicationCommand:
    def __init__(self, data: dict):
        self.id: str = data["id"]
        self.type: int = data["type"]
        self.application_id: str = data["application_id"]
        self.guild_id: Optional[str] = data["guild_id"] or None
        self.name: str = data["name"]
        self.description: str = data["description"]
        self.default_permissions: bool = data["default_permissions"]
        self.version: str = data["version"]

class Attachment:
    def __init__(self, data: dict):
        self.id: str = data["id"]
        self.file_name: str = data["filename"]
        self.description: Optional[str] = data["description"] or None
        self.content_type: Optional[str] = data["content_type"] or None
        self.size: int = data["size"]
        self.proxy_url: str = data["proxy_url"]
        self.width: Optional[int] = data["width"] or None
        self.height: Optional[int] = data["height"] or None
        self.ephemeral: Optional[bool] = data["ephemeral"] or None

class GuildChannel(BaseChannel):
    def __init__(self, client, data: dict):
        super().__init__(client, data)
        if data["type"] == 0:
            return TextBasedChannel(client, data)
        self.guild_id: str = data["guild_id"]
        self.position: int = data["position"]
        self.nsfw: bool = data["nsfw"]
        self.permission_overwrites: List[dict] = data["permission_overwrites"]
        self.parent_id: str = data["parent_id"]
        self.name: str = data["name"]
        
    async def delete(self, *, reason: Optional[str] = None) -> None:
        if reason:
            headers = self.client.http.headers.copy()
            if reason:
                headers["reason"] = reason
            
        response = await self.client.http.delete(f"/channels/{self.id}", headers=headers)
        return await response.json()
    
    async def fetch_invites(self): 
        response = await self.client.http.get(f"/channels/{self.id}/invites")
        return await response.json()
    
    async def create_invite(self, *, max_age: Optional[int], max_uses: Optional[int], temporary: Optional[bool], unique: Optional[bool], target_type: Optional[int], target_user_id: Optional[str], target_application_id: Optional[str]):
        data = {}
        data["max_age"] = max_age or None
        data["max_uses"] = max_uses or None
        data["temporary"] = temporary or None
        data["unique"] = unique or None
        data["target_type"] = target_type or None
        data["target_user_id"] = target_user_id or None
        data["target_application_id"] = target_application_id or None
        await self.client.http.post(f"/channels/{self.id}/invites", json=data)   
        
    async def delete_overwrite(self, overwrites: Overwrite) -> None:
        response = await self.client.http.delete(f"/channels/{self.id}/permissions/{overwrites.id}")
        return await response.json()
    
        
    async def fetch_pinned_messages(self) -> List[Message]:
        response = await self.client.http.get(f"/channels/{self.id}/pins")
        data = await response.json()
        return [Message(message) for message in data]
    

    
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

class GuildTextChannel(GuildChannel, Messageable):
    def __init__(self, client, data: dict):
        super().__init__(client, data)
        self.topic: str = data["topic"]
        self.rate_limit_per_user: int = data["rate_limit_per_user"]
        self.last_message_id: str = data["last_message_id"]
        self.default_auto_archive_duration: int = data["default_auto_archive_duration"]
    
    async def create_webhook(self,*, name: str, avatar: Optional[str] = None, reason: Optional[str] = None):
        headers = client.http.headers.clone()
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        

    async def start_thread(self, name: str,* , auto_archive_duration: Optional[int], type: Optional[int], invitable: Optional[bool], rate_limit_per_user: Optional[int], reason: Optional[str]):
        data = {"name": name}
        if auto_archive_duration:
            data["auto_archive_duration"] = auto_archive_duration
        if type:
            data["type"] = type
        if invitable is not None: # Geez having a bool is gonna be a pain
            data["invitable"] = invitable
        if rate_limit_per_user:
            data["rate_limit_per_user"] = rate_limit_per_user
        
        headers = self.client.http.headers.copy()
        headers["X-Audit-Log-Reason"] = reason
        
        response = await self.client.http.post(f"/channels/{self.id}/threads", data=data, headers=headers)
        self.client.guilds[self.guild_id].append(Thread(await response.json()))
    
    async def bulk_delete(self, message_ids: List[str], reason: Optional[str]) -> None:

        if reason:
            headers = self.client.http.headers.copy()
            headers["X-Audit-Log-Reason"] = reason
            
        response = await self.client.http.post(f"channels/{self.id}/messages/bulk-delete", data={"messages": message_ids}, headers=headers)
        return await response.json()

    async def list_public_archived_threads(self,*, before: Optional[str], limit: Optional[int]) -> Dict[str, Union[List[Messageable], List[ThreadMember], bool]]: # It returns a List of Threads but I can't typehint that...
        response = await self.client.http.get(f"/channels/{self.id}/threads/archived/public",params={"before": before, "limit": limit})
        return await response.json()
    
    async def list_private_archived_threads(self,*, before: Optional[str], limit: Optional[int]) -> Dict[str, Union[List[Messageable], List[ThreadMember], bool]]: # It returns a List of Threads but I can't typehint that...
        response = await self.client.http.get(f"/channels/{self.id}/threads/archived/private",params={"before": before, "limit": limit})
        return await response.json()
    
    async def list_joined_private_archived_threads(self,*, before: Optional[str], limit: Optional[int]) -> Dict[str, Union[List[Messageable], List[ThreadMember], bool]]:
        response = await self.client.http.get(f"/channels/{self.id}/threads/archived/private",params={"before": before, "limit": limit})
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
        self.default_auto_archive_duration: int = data["default_auto_archive_duration"]

    async def follow(self, webhook_channel_id: str):
        response = await self.client.http.post(f"/channels/{self.id}/followers", data={"webhook_channel_id": webhook_channel_id})
        return await response.json()

class VoiceChannel(GuildChannel):
    def __init__(self, client, data: dict):
        super().__init__(client, data)
        self.bitrate: int = data["bitrate"]
        self.user_limit: int = data["user_limit"]
        self.rtc_region: str = data["rtc_region"]
            
class DMChannel(BaseChannel):
    def __init__(self, client, data: dict):
        super().__init__(client, data)
        self.recipient: List[PartialUser] = PartialUser(data["recipient"])

class ChannelCategory(GuildChannel):
    def __init__(self, client, data: dict):
        super().__init__(client, data)

class GuildStoreChannel(GuildChannel):
    def __init__(self, client, data: dict):
        super().__init__(client, data)
        
            
class GuildNewsThread(Thread, GuildNewsChannel):
    def __init__(self, client, data: dict):
        super().__init__(client, data)

class GuildStageChannel(BaseChannel):
    def __init__(self, client, data: dict):
        super().__init__(client, data)
        self.guild_id: str = data["guild_id"]
        self.channel_id: str = data["channel_id"]
        self.privacy_level: int = data["privacy_level"]
        self.discoverable_disabled: bool = data["discoverable_disabled"]

class TextBasedChannel(BaseChannel):
    def __init__(self, client, data: dict):
        super().__init__(data)
        if self.type == 0:
            return GuildTextChannel(client, data)
        
        elif self.type == 1:
            return DMChannel(data)

        elif self.type == 4:
            return ChannelCategory(client, data)
        
        elif self.type == 5:
            return GuildNewsChannel(client, data)
        
        elif self.type == 6:
            return GuildStoreChannel(client, data)
        
        elif self.type == 10:
            return GuildNewsThread(client, data)
        
        elif self.type == 11 or self.type == 12:
            return Thread(client, data)
        
        elif self.type == 13:
            return GuildStageChannel(client, data)

class HTTPClient(ClientSession):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_uri: str = "https://discord.com/api/v9"

    async def get(self, url, *args, **kwargs):
        if url.startswith("/"):
            url = url[1:]
        return await self.session.get(f"{self.base_uri}{url}", *args, **kwargs)

    async def post(self, url, *args, **kwargs):
        if url.startswith("/"):
            url = url[1]
        return await self.session.post(f"{self.base_uri}{url}", *args, **kwargs)

    async def patch(self, url, *args, **kwargs):
        if url.startswith("/"):
            url = url[1:]
        return await self.session.patch(f"{self.base_uri}{url}", *args, **kwargs)

    async def delete(self, url, *args, **kwargs):
        if url.startswith("/"):
            url = url[1:]
        return await self.session.delete(f"{self.base_uri}{url}", *args, **kwargs)

    async def put(self, url, *args, **kwargs):
        if url.startswith("/"):
            url = url[1:]
        return await self.session.put(f"{self.base_uri}{url}", *args, **kwargs)

    async def head(self, url, *args, **kwargs):
        if url.startswith("/"):
            url = url[1:]
        return await self.session.head(f"{self.base_uri}{url}", *args, **kwargs)

class Section:
    def __init__(self):
        self.commands = {}
        self.events = {}
    
    def event(self, event_name: str):
        def register_event(func):
            self.events[event_name] = func
        return register_event

    def slash_command(self,*, name: str, description: Optional[str], options: List[Union[Subcommand, SubCommandGroup, StringOption, IntegerOption, BooleanOption, UserOption, ChannelOption, RoleOption, MentionableOption, NumberOption]]):
        def register_slash_command(func):
            self.commands[name] = {
                "callback": func,
                "name": name,
                "description": description,
                "options": options
            }
        return register_slash_command


class Client(WebsocketClient):

    def __init__(self, token: str, intents: int = 0, **options):
        super().__init__(token, intents)
        
        self.commands: List[ApplicationCommand] = []
        
        self.options: dict = options

        self.http = HTTPClient(
            headers = {
                "Authorization": f"Bot {token}"}
            )
        
        self.user: ClientUser = None
        self.application: Application = None

    def command(self, *, name: str, description: str, guild_ids: List[str], options: Union[Subcommand, SubCommandGroup, StringOption, IntegerOption, BooleanOption, UserOption, ChannelOption, RoleOption, MentionableOption, NumberOption]):
        def register_slash_command(func):
            self.commands[func.__name__] = {"callback": func, "name": name, "description": description, "guild_ids": guild_ids, "options": options}
        return register_slash_command

    def add_section(self, section: Section):
        if not isinstance(section, Section):
            raise InvalidArgumentType("You must pass in a class that inherits from the Section class.")
        for name, command_object in section.commands:
            self.commands[name] = command_object

        for event_name, event_func in section.events:
            self.events[event_name.lower().replace("on_")] = event_func
        
        # Successfully extracted all the valuable stuff from the section        
# class ClientGuildMember(Member):
#     def __init__(self, client: Client,data: dict):
#         super().__init__(data)
class Colour:
    #some of this code is sourced from discord.py, rest assured all the colors are different from discord.py
    __slots__ = ('value',)

    def __init__(self, value: int):
        if not isinstance(value, int):
            raise TypeError(f'Expected int parameter, received {value.__class__.__name__} instead.')

        self.value: int = value

    def _get_byte(self, byte: int) -> int:
        return (self.value >> (8 * byte)) & 0xff

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Colour) and self.value == other.value

    def __ne__(self, other: Any) -> bool:
        return not self.__eq__(other)

    def __str__(self) -> str:
        return f'#{self.value:0>6x}'

    def __int__(self) -> int:
        return self.value

    def __repr__(self) -> str:
        return f'<Colour value={self.value}>'

    def __hash__(self) -> int:
        return hash(self.value)

    @property
    def r(self) ->int:
        """Return the red component in rgb"""
        return self._get_byte(2)

    @property
    def g(self) ->int:
        """Return the green component in rgb"""
        return self._get_byte(1)

    @property
    def b(self) ->int:
        """Return the blue component in rgb"""
        return self._get_byte(0)

    def to_rgb(self) -> Tuple[int, int, int]:
        """returns an rgb color as a tuple"""
        return (self.r, self.g,self.b)

    @classmethod
    def from_rgb(cls: Type[CT], r: int, g: int, b: int) -> CT:
        """Constructs a :class:`Colour` from an RGB tuple."""
        return cls((r << 16) + (g << 8) + b)

    @classmethod
    def lime_green(cls: Type[CT]) -> CT:
        """Returns a color of lime green"""
        return cls(0x00ff01)

    @classmethod
    def light_green(cls: Type[CT]) -> CT:
        """Returns a color of light green"""
        return cls(0x00ff22)

    @classmethod
    def dark_green(cls: Type[CT]) -> CT:
        """Returns a color of dark green"""
        return cls(0x00570a)
    
    @classmethod
    def light_blue(cls: Type[CT]) -> CT:
        """Returns a color of light blue"""
        return cls(0x00ff01)

    @classmethod
    def dark_blue(cls: Type[CT]) -> CT:
        """Returns a color of dark blue"""
        return cls(0x0a134b)

    @classmethod
    def light_red(cls: Type[CT]) -> CT:
        """Returns a color of light red"""
        return cls(0xaa5b54)

    @classmethod
    def dark_red(cls: Type[CT]) -> CT:
        """Returns a color of dark red"""
        return cls(0x4c0000)
    
    @classmethod
    def black(cls: Type[CT]) -> CT:
        """Returns a color of black"""
        return cls(0x00000)

    default=black
    @classmethod
    def white(cls: Type[CT]) -> CT:
        return cls(0xffffff)
Color=Colour

class MessageSelectMenuOption:
    def __init__(self, label: str, value: str, description: Optional[str], emoji: Optional[PartialEmoji], default: Optional[bool]):
        self.settings = {
            "label": label,
            "value": value,
            "description": description or None,
            "emoji": emoji or None,
            "default": default or None            
        }
    
    def __repr__(self):
        return self.settings

class MessageSelectMenu(BaseComponent):
    def __init__(self):
        self.settings = {
            "options": [], 
            "type": 3,
            "min_values": 1,
            "max_values": 1,
            "disabled": False
        }
    
    def __repr__(self):
        return self.settings

    def add_options(self, options: List[MessageSelectMenuOption]):
        for option in options:
            
            if len(self.settings["options"] > 25):
                raise TooManySelectMenuOptions("You can only have 25 options in a select menu.")
            
            self.settings["options"].append(option.data)
        return self
        
    def set_placeholder(self, placeholder: str):
        if not isinstance(placeholder, str):
            raise InvalidArgumentType("Placeholder must be a string.")
        
        self.settings["placeholder"] = placeholder
        return self
    
    def set_min_values(self, min: int):
        if not isinstance(min, int):
            raise InvalidArgumentType("Min must be an integer.")
        
        self.options["min_values"] = min
        return self


    def set_max_values(self, max: int):
        if not isinstance(max, int):
            raise InvalidArgumentType("Max must be an integer.")
        
        self.options["max_values"] = max  
        return self  


class MessageButton(BaseComponent):
    def __init__(self,*, style: Optional[Union[int, str]] = 1, label: Optional[str], emoji: Optional[Union[PartialEmoji, dict]], url: Optional[str]):
        self.settings = {
            "type": 2,
            "style": style or 1,
            "label": label or "Click me!",
            "emoji": None,
            "disabled": False,
        }
        if url:
            self.settings["url"] = url
            self.settings["style"] = 5
        if emoji:
            self.settings["emoji"] = emoji
    def __repr__(self):
        return self.settings

    def set_label(self, label: str):

        if not isinstance(label, str):
            raise InvalidArgumentType("Label must be a string.")
        
        if len(label) > 80:
            raise LabelIsTooBig("Label must be 80 characters or less.")
            
        self.settings["label"] = label
        return self
    
    def set_style(self, style: Union[int, str]):
        valid_styles = {
            "PRIMARY": 1,
            "SECONDARY": 2,
            "SUCCESS": 3,
            "DANGER": 4,
            "LINK": 5
        }
        if isinstance(style, str):
            if style.upper() not in valid_styles:
                raise InvalidMessageButtonStyle("Invalid button style. Style must be one of PRIMARY, SECONDARY, LINK, DANGER, or SUCCESS.")
            self.settings["style"] = valid_styles[style.upper()]
            return self
            
        elif isinstance(style, int):
            if style not in valid_styles.values():
                raise InvalidMessageButtonStyle("Invalid button style. Style must be in range 1 to 5 inclusive.")
            self.settings["style"] = style
            return self
    def set_emoji(self, emoji: Union[PartialEmoji, dict]):

        if isinstance(emoji, dict):
            self.settings["emoji"] = emoji
            return self

        elif isinstance(emoji, PartialEmoji):
            self.settings["emoji"] = emoji.data
            return self
        raise InvalidArgumentType("Emoji must be a PartialEmoji or a dict that represents a PartialEmoji.")
                    
    def set_url(self, url: str):
        
        if not isinstance(url, str):
            raise InvalidArgumentType("Url must be a string.")
        
        self.settings["url"] = url
        self.settings["style"] = 5
        return self

        

class MessageActionRow:
    def __init__(self, components: Optional[List[Union[MessageButton, MessageSelectMenu]]]):
        self.settings = {
            "type": 1,
            "components": components
        }

    def __repr__(self):
        return self.settings
        
    def add_components(self, components: List[Union[MessageButton, MessageSelectMenu]]):
        buttons = 0
        for component in self.settings["components"]:
            if type(component) == MessageButton:
                buttons += 1
            
            elif buttons > 5:
                raise TooManyComponents("You can only have 5 buttons per row.")
            
            elif type(component) == MessageSelectMenu:
                raise TooManyComponents("You can only have 1 select menu per row. No buttons along that select menu.")
        self.settings["components"].append(components)
        return self

class EmbedAuthor:
    def __init__(self, data: dict):
        self.name: str = data["name"]
        self.url: Optional[str] = data["url"] or None
        self.icon_url: Optional[str] = data["icon_url"] or None
        self.proxy_icon_url: Optional[str] = data["proxy_icon_url"] or None

class Embed: # Always wanted to make this class :D
    def __init__(self,*, title: Optional[str], description: Optional[str], color:Optional[Colour], colour:Optional[Colour], url:Optional[str]):
        
        self.title: Optional[str] = title
        self.type: Optional[str] = type
        self.description: Optional[str] = description
        self.url: Optional[str] = url
        self.timestamp: Optional[str] = None
        self.color: Optional[Colour] = color or colour
        self.footer: Optional[str] = None
        self.image: Optional[str] = None
        self.thumbnail: Optional[str] = None
        self.valid_styles: Optional[str] = None
        self.provider: Optional[str] = None
        self.author: Optional[EmbedAuthor] = None
        self.fields: Optional[List[str]] = None
        
    def add_field(self,*, name: str, value: str, inline: bool = False):
        self.fields.append({"name": name, "value": value, "inline": inline})
        
    def set_thumbnail(self, url: str):
        self.thumbnail = url
    
    def set_image(self, url:str):
        self.image = url
    
    def set_footer(self, footertxt:str):
        self.footer = footertxt

    def set_author(self, author:EmbedAuthor):
        self.author = author

    def set_timestamp(self, timestamp):
        pass #someone do this??

    @property
    def fields(self):
        return self.fields #needs improvement

class Emoji:
    def __init__(self, client, data: dict):
        self.id: Optional[str] = data["id"]
        self.name: Optional[str] = data["name"]
        self.roles: List[Role] = [Role(role) for role in data["roles"]]
        self.user: Optional[User] = User(data["user"]) if "user" in data else None
        self.requires_colons: bool = data["require_colons"]
        self.managed: bool = data["managed"]
        self.animated: bool = data["animated"]
        self.available: bool = data["available"]
class DiscordAPIError(Exception): # 
    ...
    
class InvalidToken(Exception):
    ...

class UnhandledException(Exception):
    ... 



class BadRequest400(Exception):
    ...

class Unauthorized401(Exception):
    ...

class Forbidden403(Exception):
    ...

class NotFound404(Exception):
    ...

class MethodNotAllowed405(Exception):
    ...
    
class Ratelimited429(Exception):
    ...

class GateawayUnavailable502(Exception):
    ...
    
class InternalServerError5xx(Exception):
    ...
    
class TooManyComponents(Exception):
    ...

class InvalidMessageButtonStyle(Exception):
    ...

class CustomIdIsTooBig(Exception):
    ...

class InvalidArgumentType(Exception):
    ...

class TooManySelectMenuOptions(Exception):
    ...
    
class LabelIsTooBig(Exception):
    ...
    
class ThreadArchived(Exception):
    ...

class WelcomeChannel:
    def __init__(self, data: dict):
        self.channel_id: str = data["channel_id"]
        self.description: str = data["description"]
        self.emoji_id: Optional[str] = data["emoji_id"]
        self.emoji_name: Optional[str] = data["emoji_name"]

class WelcomeScreen:
    def __init__(self, data: dict):
        self.description: Optional[str] = data["description"] or None
        self.welcome_channels: List[WelcomeChannel] = [WelcomeChannel(welcome_channel) for welcome_channel in data["welcome_channels"]]

class Guild:
    def __init__(self, client: Client, data: dict):
        self.client = client
        self.data: dict = data
        self.id: str = data["id"]
        self.name: str = data["name"]
        self.icon: Optional[str] = data["icon"] or None
        self.icon_hash: Optional[str] = data["icon_hash"] or None
        self.splash: Optional[str] = data["splash"] or None
        self.discovery_splash: Optional[str] = data["discovery_splash"] or None
        self.owner_id: str = data["owner_id"]
        self.permissions: str = data["permissions"]
        self.afk_channel_id: str = data["afk_channel_id"]
        self.afk_timeout: int = data["afk_timeout"]
        self.verification_level: str = "NONE" if data["verification_level"] == 0 else "LOW" if data["verification_level"] == 1 else "MEDIUM" if data["verification_level"] == 2 else "HIGH" if data["verification_level"] == 3 else "VERY_HIGH"
        self.default_message_notifications: str = "ALL" if data["default_message_notifications"] == 0 else "MENTIONS" 
        self.explicit_content_filter: str = "DISABLED" if data["explicit_content_filter"] == 0 else "MEMBERS_WITHOUT_ROLES" if data["explicit_content_filter"] == 1 else "ALL_MEMBERS"
        self.roles: List[Role] = [Role(role) for role in data["roles"]]
        self.emojis: List[Emoji] = [Emoji(emoji) for emoji in data["emojis"]]
        self.features: List[str] = data["features"]
        self.mfa_level: str = "NONE" if data["mfa_level"] == 0 else "ELEVATED"
        self.application_id: Optional[str] = data["application_id"] or None
        self.system_channel_id: Optional[str] = data["system_channel_id"] or None
        self.system_channel_flags: int = data["system_channel_flags"]
        self.rules_channel_id: Optional[int] = data["rules_channel_id"] or None
        self.joined_at: Optional[str] = data["joined_at"] or None
        self.large: bool = data["large"]
        self.unavailable: bool = data["unavailable"]
        self.member_count: int = data["member_count"]
        # self.voice_states: List[dict] = data["voice_states"]
        self.members: List[GuildMember] = [GuildMember(member) for member in data["members"]]
        self.channels: List[GuildChannel] = [GuildChannel(channel) for channel in data["channels"]]
        self.threads: List[Thread] = [Thread(thread) for thread in data["threads"]]
        self.presences: List[dict] = data["presences"]
        self.max_presences: int = data["max_presences"]
        self.max_members: int = data["max_members"]
        self.vanity_url_code: Optional[str] = data["vanity_url_code"] or None
        self.description: Optional[str] = data["description"] or None
        self.banner: Optional[str] = data["banner"] or None
        self.premium_tier: int = data["premium_tier"]
        self.premium_subscription_count: int = data["premium_subscription_count"]
        self.preferred_locale: str = data["preferred_locale"]
        self.public_updates_channel_id: Optional[str] = data["public_updates_channel_id"] or None
        self.max_video_channel_users: Optional[int] = data["max_video_channel_users"] or None
        self.approximate_member_count: Optional[int] = data["approximate_member_count"] or None
        self.approximate_presence_count: Optional[int] = data["approximate_presense_count"] or None
        self.welcome_screen: Optional[WelcomeScreen] = WelcomeScreen(data["welcome_screen"]) if data["welcome_screen"] else None
        self.nsfw_level: int = data["nsfw_level"]
        self.stage_instances: List[GuildStageChannel] = [GuildStageChannel(channel) for channel in data["stage_instances"]]
        self.stickers: Optional[StickerItem] = StickerItem(data["stickers"]) if data["stickers"] else None

class GuildScheduledEvent:
    def __init__(self, client: Client, data: dict):
        self.id: str = data["id"]
        self.client = client
        self.guild_id: str = data["guild_id"]
        self.channel_id: Optional[str] = data["channel_id"] or None
        self.creator_id: Optional[str] = data["creator_id"] or None
        self.name: str = data["name"]
        self.description: Optional[str] = data["description"] or None
        self.scheduled_start_time: str = data["scheduled_start_time"]
        self.scheduled_end_time: Optional[str] = data["scheduled_end_time"] or None
        self.privacy_level: int = data["privacy_level"]
        self.status: str = "SCHEDULED" if data["status"] == 1 else "ACTIVE" if data["status"] == 2 else "COMPLETED" if data["status"] == 3 else "CANCELLED"
        self.entity_type: str = "STAGE_INSTANCE" if data["status"] == 1 else "VOICE" if data["status"] == 2 else "EXTERNAL"
        self.entity_id: str = data["entity_id"]
        self.entity_metadata: dict = data["entity_metadata"]
        self.creator: Optional[User] = User(data["creator"]) or None
        self.user_count: Optional[int] = data["user_count"] or None

class WebhookUser:
    def __init__(self, data: dict):
        self.webhook_id: str = data["webhook_id"]
        self.username: str = data["username"]
        self.avatar: str = data["avatar"]


class Webhook:
    def __init__(self, client, data: dict = None):
        """
        Don't pass in data if you're making a webhook, the lib passes data to construct an already existing webhook
        """
        self.client = client
        self.data = data
        if data:
            self.id: str = data["id"] 
            self.type: str = "Incoming" if data["type"] == 1 else "Channel Follower" if data["type"] == 2 else "Application"
            self.guild_id: Optional[str] = data["guild_id"] or None
            self.channel_id: Optional[str] = data["channel_id"] or None
            self.user: Optional[User] = User(client, data["user"])
            self.name: Optional[str] = data["name"] or None
            self.avatar: Optional[str] = data["avatar"] or None
            self.token: Optional[str] = data["token"] or None
            self.application_id: Optional[str] = data["application_id"] or None
            self.source_guild: Optional[PartialGuild] = PartialGuild(data["source_guild"])
            self.url: Optional[str] = data["url"]
    
class BaseInteraction:
    def __init__(self, client, data: dict):
        self.id: str = data["id"]
        self.client = client
        self.application_id: int = data["application_id"]
        self.type: int = data["type"]
        self.data: Optional[dict] = data["data"] or None
        self.guild_id: Optional[str] = data["guild_id"] or None
        self.channel_id: Optional[str] = data["channel_id"] or None
        self.member: Optional[GuildMember] = GuildMember(data["member"]) or None
        self.user: Optional[User] = User(data["user"]) or None
        self.token: str = data["token"]
        self.version: int = data["version"]
        self.locale: Optional[str] = data["locale"] or None
        self.guild_locale: Optional[str] = data["guild_locale"] or None
        
    def is_ping(self):
        return self.type == 1
    
    def is_application_command(self):
        return self.type == 2
    
    def is_message_component(self):
        return self.type == 3
    
    def is_autocomplete(self):
        return self.type == 4
    
    async def reply(self, message_data: dict):
        response = await self.client.http.post(f"/interactions/{self.id}/{self.token}/callback", data=message_data)
        return await response.json()
    
    async def fetch_reply(self):
        response = await self.client.http.get(f"/webhooks/{self.application_id}/{self.token}/{self.token}/messages/@original")
        return await response.json()
    
    async def edit_reply(self, message_data: dict):
        response = await self.client.http.patch(f"/webhooks/{self.application_id}/{self.token}/messages/@original", data=message_data)
        return await response.json()
    
    async def delete_reply(self):
        response = await self.client.http.delete(f"/webhooks/{self.application_id}/{self.token}/messages/@original")
        return await response.json()
    
    async def followup(self, message_data: dict):
        response = await self.client.http.post(f"/webhooks/{self.application_id}/{self.token}", data=message_data)
        return await response.json()
    
    async def fetch_followup_message(self, message_id: str):
        response = await self.client.http.get(f"/webhooks/{self.application_id}/{self.token}/messages/{message_id}")
        return await response.json()
    
    async def edit_followup(self, message_id: str, message_data):
        response = await self.client.http.patch(f"/webhooks/{self.application_id}/{self.token}/messages/{message_id}", data=message_data)
        return await response.json()
    
    async def delete_followup(self, message_id: str):
        response = await self.client.http.delete(f"/webhooks/{self.application_id}/{self.token}/messages/{message_id}")
        return await response.json()

class Invite:
    def __init__(self, data: dict):
        self.code: str = data["code"]
        self.guild: Optional[PartialGuild] = PartialGuild(data["guild"]) or None
        self.channel: GuildChannel = GuildChannel(data["channel"]) 
        self.inviter: Optional[User] = User(data["inviter"]) or None
        self.target_type: int = data["target_type"]
        self.target_user: Optional[User] = User(data["target_user"]) or None
        self.target_application: Optional[Application] = Application(data["target_application"]) or None
        self.approximate_presence_count: Optional[int] = data["approximate_presence_count"] or None
        self.approximate_member_count: Optional[int] = data["approximate_member_count"] or None
        self.expires_at: Optional[str] = data["expires_at"] or None
        self.stage_instance: Optional[GuildStageChannel] = GuildStageChannel(data["stage_instance"]) or None
        self.guild_scheduled_event: Optional[GuildScheduledEvent] = GuildScheduledEvent(data["guild_scheduled_event"]) or None
    # Dabmaster is gonna work on this

class GuildMember:
    def __init__(self, client, data: dict):
        self.data = data
        self.client = client
        # self.user: Optional[User] = User(data["user"]) or None
        self.nick: Optional[str] = data["nick"] or None
        self.avatar: Optional[str] = data["avatar"] or None
        self.roles: List[Role] = [role.Role(role) for role in data["roles"]]
        self.joined_at:str = data["joined_at"]
        self.premium_since: Optional[str] = data["premium_since"] or None
        self.deaf: bool = data["deaf"]
        self.mute: bool = data["mute"]
        self.pending: Optional[bool] = data["pending"] or None
        self.permissions: Optional[str] = data["permissions"] or None
        self.communication_disabled_until: Optional[str] = data["communication_disabled_until"] or None

class MentionedChannel:
    def __init__(self, data: dict):
        self.id: str = data["id"]
        self.guild_id: str = data["guild_id"]
        self.type: int = data["type"]
        self.name: str = data["name"]
        
class MentionedUser(User):
    def __init__(self, client, data: dict):
        super().__init__(client, data)
        self.member = GuildMember(data["member"])

class MessageActivity:
    def __init__(self, data: dict):
        self.type: int = data["type"]
        self.party_id: Optional[str] = data["party_id"]

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
        self.id: str = data["id"]
        self.type: int = data["type"]
        self.name: str = data["name"]
        self.user: User = User(client, data["user"])
        self.member: GuildMember = GuildMember(client, data["member"])

    def is_ping(self):
        return self.type == 1
    
    def is_application_command(self):
        return self.type == 2
    
    def is_message_component(self):
        return self.type == 3
    
    def is_autocomplete(self):
        return self.type == 4
    
    async def reply(self, message_data: dict):
        response = await self.client.http.post(f"/interactions/{self.id}/{self.token}/callback", data=message_data)
        return await response.json()
    
    async def fetch_reply(self):
        response = await self.client.http.get(f"/webhooks/{self.application_id}/{self.token}/{self.token}/messages/@original")
        return await response.json()
    
    async def edit_reply(self, message_data: dict):
        response = await self.client.http.patch(f"/webhooks/{self.application_id}/{self.token}/messages/@original", data=message_data)
        return await response.json()
    
    async def delete_reply(self):
        response = await self.client.http.delete(f"/webhooks/{self.application_id}/{self.token}/messages/@original")
        return await response.json()
    
    async def followup(self, message_data: dict):
        response = await self.client.http.post(f"/webhooks/{self.application_id}/{self.token}", data=message_data)
        return await response.json()
    
    async def fetch_followup_message(self, message_id: str):
        response = await self.client.http.get(f"/webhooks/{self.application_id}/{self.token}/messages/{message_id}")
        return await response.json()
    
    async def edit_followup(self, message_id: str, message_data):
        response = await self.client.http.patch(f"/webhooks/{self.application_id}/{self.token}/messages/{message_id}", data=message_data)
        return await response.json()
    
    async def delete_followup(self, message_id: str):
        response = await self.client.http.delete(f"/webhooks/{self.application_id}/{self.token}/messages/{message_id}")
        return await response.json()

class PartialUser:
    def __init__(self, data: dict):
        self.data: dict = data
        self.id: str = data["id"]
        self.username: str = data["username"]
        self.discriminator: str = data["discriminator"]
        self.avatar: Optional[str] = data["avatar"]

class PartialGuild:
    def __init__(self, data):
        self.data: dict = data
        self.id: str = data["id"]
        self.name: str = data["name"]
        self.permissions: int = int(data["permissions"])
        self.features: List[str] = data["features"]


class RoleTag:
    def __init__(self, data: dict):
        self.bot_id: Optional[str] = data["bot_id"] or None
        self.integration_id: Optional[str] = data["integration_id"] or None
        self.premium_subscriber: Optional[bool] = data["premium_subscriber"] or None
class Role:
    def __init__(self, client, data: dict):
        self.data = data
        self.client = client
        self.id: str = data["id"]
        self.name: str = data["name"]
        self.color: int = data["color"]
        self.hoist: bool = data["hoist"]
        self.icon: Optional[str] = data["icon"] or None
        self.unicode_emoji: Optional[str] = data["unicode_emoji"] or None
        self.position: int = data["position"]
        self.permissions: str = data["permissions"] # Permissions soon
        self.managed: bool = data["managed"]
        self.mentionable: bool = data["mentionable"]
        self.tags: RoleTag = RoleTag(self.data["tags"])

class SlashCommand(ApplicationCommand):
    def __init__(self, data: dict):
        super().__init__(data)
        self.options: Optional[List[Union[Subcommand, SubCommandGroup, StringOption, IntegerOption, BooleanOption, UserOption, ChannelOption, RoleOption, MentionableOption, NumberOption]]] = data["options"] or None # Return the type hinted class later this will take too long and is very tedious, I'll probably get Copilot to do it for me lmaofrom .stickers import *
class TeamMember:
    def __init__(self, data: dict):
        self.data = data
        self.membership_state: int = data["membership_state"]
        self.team_id: str = data["team_id"]
        self.user: PartialUser = PartialUser(data["user"])

class Team:
    def __init__(self,data: dict):
        self.data = data
        self.icon: str = data["icon"]
        self.id: str = data["id"]
        self.members: List[TeamMember] = data["members"]

class ClientUser():
    
    def __init__(self, client, data: dict):
        self.client = client
        self.data = data
        self.verified: bool = data["verified"]
        self.username: str = data["username"]
        self.mfa_enabled: bool = data["mfa_enabled"]
        self.id: str = data["id"]
        self.flags: int = data["flags"]
        self.email: Optional[str] = data["email"] or None
        self.discriminator: str = data["discriminator"]
        self.bot: bool = data["bot"]
        self.avatar: str = data["avatar"]
        if not self.bot: # if they're a user account
            print("Self botting is against Discord ToS. You can get ban.") # Yeah I'm keeping this as a print
    async def fetch(self):
        response = await self.client.http.get("users/@me")
        data = await response.json()
        super().__init__(data) # Reinitialse the class with the new data.
    
    async def edit(self, *, username: Optional[str] = None, avatar: Optional[bytes] = None):
        payload = {}
        if username:
            payload["username"] = username
        if avatar:
            payload["avatar"] = _bytes_to_base64_data(avatar)
        response = await self.client.http.patch("users/@me", json=payload)
        data = await response.json()
        self.__init__(data) # Reinitialize the class with the new data, the full data.

class SourceChannel:
    def __init__(self, data: dict):
        self.id: str = data["id"]
        self.name: str = data["name"]

class Webhook: # Not used for making webhooks.
    def __init__(self, client, data: dict):
        self.id: str = data["id"]
        self.client = client
        self.type: int = "Incoming" if data["type"] == 1 else "Channel Follower" if data["type"] == 2 else "Application"
        self.guild_id: Optional[str] = data["guild_id"]
        self.channel_id: Optional[str] = data["channel_id"]
        self.user: Optional[WebhookUser] = WebhookUser(data["user"])
        self.name: Optional[str] = data["name"]
        self.avatar: Optional[str] = data["avatar"]
        self.token: str = data["token"]
        self.application_id: Optional[str] = data["application_id"]
        self.source_guild: Optional[PartialGuild] = PartialGuild(data["source_guild"])
        self.source_channel: Optional[SourceChannel] = SourceChannel(data["source_channel"]) or None
        self.url: Optional[str] = data["url"]

class Message:
    def __init__(self, client, data: dict):
        self.client = client
        self.id: str = data["id"]
        self.channel_id: str = data["channel_id"]
        self.channel: Messageable = Messageable(self.client, data["channel_id"])
        self.guild_id: Optional[str] = data["guild_id"] or None
        self.webhook_id: Optional[str] = data["webhook_id"] or None
        self.author: Optional[User] if not self.webhook_id else WebhookUser = WebhookUser(data["author"]) if self.webhook_id else User(data["author"])
        self.member: Optional[GuildMember] = GuildMember(data["member"]) if data["member"] else None
        self.content: Optional[str] = data["content"] or None # I forgot Message Intents are gonna stop this.
        self.timestamp: str = data["timestamp"]
        self.edited_timestamp: Optional[str] = data["edited_timestamp"] or None
        self.tts: bool = data["tts"]
        self.mention_everyone: bool = data["mention_everyone"]
        self.mentions: Optional[List[MentionedUser]] = [MentionedUser(mention) for mention in data["mentions"]] or None
        self.mention_roles: Optional[List[int]] = data["mention_roles"] or None
        self.mention_channels: Optional[List[MentionedChannel]] = [MentionedChannel(channel) for channel in data["mention_channels"]] or None
        self.embeds: Optional[List[Embed]] = [Embed(embed) for embed in data["embeds"]] or None
        self.reactions: Optional[List[Reaction]] = [Reaction(reaction) for reaction in data["reactions"]] or None
        self.nonce: Optional[Union[int, str]] = data["nonce"] or None
        self.pinned: bool = data["pinned"]
        self.type: int = data["type"]
        self.activity: MessageActivity = MessageActivity(data["activity"])
        self.application: Application = Application(data["application"]) # Despite there being a PartialApplication, Discord don't specify what attributes it has
        self.flags: int = data["flags"]
        self.referenced_message: Optional[Message] = Message(data["referenced_message"]) if data["referenced_message"] else None
        self.interaction: Optional[MessageInteraction] = MessageInteraction(client, data["interaction"]) if data["interaction"] else None
        self.thread: Thread = Thread(data["thread"]) if data["thread"] else None
        self.components: Optional[List[Union[MessageSelectMenu, MessageButton]]] = [MessageSelectMenu(component) if component["type"] == 1 else MessageButton(component) for component in data["components"]] or None
        self.stickers: Optional[List[StickerItem]] = [StickerItem(sticker) for sticker in data["stickers"]] or None
        
    async def add_reaction(self, emoji: str):
        emoji = quote(emoji)
        response = await self.client.http.put(f"channels/{self.channel_id}/messages/{self.id}/reactions/{emoji}/@me")
        return await response.json()
    
    async def remove_reaction(self, emoji: str, user: Optional[User] = None):
        emoji = quote(emoji)
        if not user:        
            response = await self.client.http.delete(f"channels/{self.channel_id}/messages/{self.id}/reactions/{emoji}/@me")
        else:
            response = await self.client.http.delete(f"channels/{self.channel_id}/messages/{self.id}/reactions/{emoji}/{user.id}")
        return await response.json()
    
    async def fetch_reactions(self,*, after, limit) -> List[Reaction]:
        response = await self.client.http.get(f"channels/{self.channel_id}/messages/{self.id}/reactions?after={after}&limit={limit}")
        return await response.json()
    
    async def delete_all_reactions(self):
        response = await self.client.http.delete(f"channels/{self.channel_id}/messages/{self.id}/reactions")
        return await response.json()
    
    async def delete_reaction_for_emoji(self, emoji: str):
        emoji = quote(emoji)
        response = await self.client.http.delete(f"channels/{self.channel_id}/messages/{self.id}/reactions/{emoji}")
        return await response.json()
    
    async def edit(self, message_data: dict):
        response = await self.client.http.patch(f"channels/{self.channel_id}/messages/{self.id}", data=message_data)
        return await response.json()
    
    async def delete(self):
        response = await self.client.http.delete(f"channels/{self.channel_id}/messages/{self.id}")
        return await response.json()
    
    async def pin(self, *, reason: Optional[str]):
        headers = self.client.http.headers.copy()
        headers["X-Audit-Log-Reason"] = reason
        response = await self.client.http.put(f"channels/{self.channel_id}/pins/{self.id}", headers=headers)
        return await response.json()
    
    async def unpin(self, *, reason: Optional[str]):
        headers = self.client.http.headers.copy()
        headers["X-Audit-Log-Reason"] = reason
        response = await self.client.http.delete(f"channels/{self.channel_id}/pins/{self.id}", headers=headers)
        return await response.json()

    async def start_thread(self, name: str, auto_archive_duration: Optional[int], rate_limit_per_user: Optional[int]):
        response = await self.client.http.post(f"channels/{self.channel_id}/messages/{self.id}/threads", data={"name": name, "auto_archive_duration": auto_archive_duration, "rate_limit_per_user": rate_limit_per_user})
        self.client.guilds[self.guild_id].append(Thread(await response.json())) # Cache it
        return Thread(await response.json())
    
    async def crosspost(self):
        response = await self.client.http.post(f"channels/{self.channel_id}/messages/{self.id}/crosspost")
        return await response.json()
    
def compute_timedelta(dt: datetime.datetime):
    if dt.tzinfo is None:
        dt = dt.astimezone()
    now = datetime.datetime.now(datetime.timezone.utc)
    return max((dt - now).total_seconds(), 0)
  
  
async def sleep_until(when: Union[datetime.datetime, int, float], result: Optional[T] = None) -> Optional[T]:
    if when == datetime.datetime:
        delta = compute_timedelta(when)
    
    return await asyncio.sleep(delta if when == datetime.datetime else when, result)
  
def remove_markdown(text: str, *, ignore_links: bool = True) -> str:
    def replacement(match):
        groupdict = match.groupdict()
        return groupdict.get('url', '')

    regex = _MARKDOWN_STOCK_REGEX
    if ignore_links:
        regex = f'(?:{_URL_REGEX}|{regex})'
    return re.sub(regex, replacement, text, 0, re.MULTILINE)
  
def escape_markdown(text: str, *, as_needed: bool = False, ignore_links: bool = True) -> str:
    if not as_needed:

        def replacement(match):
            groupdict = match.groupdict()
            is_url = groupdict.get('url')
            if is_url:
                return is_url
            return '\\' + groupdict['markdown']

        regex = _MARKDOWN_STOCK_REGEX
        if ignore_links:
            regex = f'(?:{_URL_REGEX}|{regex})'
        return re.sub(regex, replacement, text, 0, re.MULTILINE)
    else:
        text = re.sub(r'\\', r'\\\\', text)
        return _MARKDOWN_ESCAPE_REGEX.sub(r'\\\1', text)
      
def escape_mentions(text: str) -> str:
    return re.sub(r'@(everyone|here|[!&]?[0-9]{17,20})', '@\u200b\\1', text)

def utcnow() -> datetime.datetime:
    return datetime.datetime.now(datetime.timezone.utc)