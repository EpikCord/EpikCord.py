from .client import Client
from .message import AllowedMention
from .components import MessageSelectMenu, MessageButton
from .embed import Embed
from .message import Message
from .partials import PartialUser
from .abc import BaseChannel
from typing import (
    List,
    Optional,
    Union
)

class GuildChannel(BaseChannel):
    def __init__(self, client: Client, data: dict):
        super().__init__(client, data)
        self.guild_id: str = data["guild_id"]
        self.position: int = data["position"]
        self.nsfw: bool = data["nsfw"]
        self.permission_overwrites: List[dict] = data["permission_overwrites"]
        self.parent_id: str = data["parent_id"]
        self.name: str = data["name"]
        
    async def delete(self, *, reason: Optional[str] = None) -> None:
        if reason:
            headers = self.client.http.headers
            headers["reason"] = reason
            
        response = await self.client.http.delete(f"channels/{self.id}", headers=headers)

    async def fetch_messages(self,*, around: Optional[str] = None, before: Optional[str] = None, after: Optional[str] = None, limit: Optional[int] = None) -> List[Message]:
        response = await self.client.http.get(f"channels/{self.id}/messages", params={"around": around, "before": before, "after": after, "limit": limit})
        data = await response.json()
        return [Message(message) for message in data]
    
    async def fetch_message(self,*, message_id: str) -> Message:
        response = await self.client.http.get(f"channels/{self.id}/messages/{message_id}")
        data = await response.json()
        return Message(data)

    async def send(self,*, content: str, tts: Optional[bool], embeds: Optional[List[Embed]], allowed_mentions: Optional[AllowedMention], message_reference: Optional[dict], components: List[Union[MessageSelectMenu, MessageButton]], sticker_ids: Optional[List[str]]) -> Message:
        response = await self.client.http.post(f"channels/{self.id}/messages", data={"content": content, "tts": tts, "embeds": embeds, "allowed_mentions": allowed_mentions, "message_reference": message_reference, "components": components, "sticker_ids": sticker_ids})
        data = await response.json()
        return Message(data)

    async def crosspost(self, message_id: str):
        response = await self.client.http.post(f"channels/{self.id}/messages/{message_id}/crosspost")
        data = await response.json()
        return Message(data)
    
    
    
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
    
class GuildTextChannel(GuildChannel):
    def __init__(self, client: Client, data: dict):
        super().__init__(client, data)
        self.topic: str = data["topic"]
        self.rate_limit_per_user: int = data["rate_limit_per_user"]
        self.last_message_id: str = data["last_message_id"]
        self.default_auto_archive_duration: int = data["default_auto_archive_duration"]
    
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
    def __init__(self, client: Client, data: dict):
        super().__init__(client, data)
        self.default_auto_archive_duration: int = data["default_auto_archive_duration"]
        
class GuildVoiceChannel(GuildChannel):
    def __init__(self, client: Client, data: dict):
        super().__init__(client, data)
        self.bitrate: int = data["bitrate"]
        self.user_limit: int = data["user_limit"]
        self.rtc_region: str = data["rtc_region"]
            
class DMChannel(BaseChannel):
    def __init__(self, client: Client, data: dict):
        super().__init__(client, data)
        self.recipient: List[PartialUser] = PartialUser(data["recipient"])

class ChannelCategory(GuildChannel):
    def __init__(self, client: Client, data: dict):
        super().__init__(client, data)

class GuildStoreChannel(GuildChannel):
    def __init__(self, client: Client, data: dict):
        super().__init__(client, data)
        
class Thread(GuildChannel):
    def __init__(self, client: Client, data: dict):
        super().__init__(client, data)
        self.owner_id: str = data["owner_id"]
        self.message_count: int = data["message_count"]
        self.member_count: int = data["member_count"]
        self.archived: bool = data["archived"]
        self.auto_archive_duration: int = data["auto_archive_duration"]
        self.archive_timestamp: str = data["archive_timestamp"]
        self.locked: bool = data["locked"]

class GuildNewsThread(Thread, GuildNewsChannel):
    def __init__(self, client: Client, data: dict):
        super().__init__(client, data)

class GuildStageChannel(BaseChannel):
    def __init__(self, client: Client, data: dict):
        super().__init__(client, data)
        self.guild_id: str = data["guild_id"]
        self.channel_id: str = data["channel_id"]
        self.privacy_level: int = data["privacy_level"]
        self.discoverable_disabled: bool = data["discoverable_disabled"]

class TextBasedChannel(BaseChannel):
    def __init__(self, client: Client, data: dict):
        super().__init__(data)
        if self.type == 0:
            return GuildTextChannel(client, data)
        
        elif self.type == 1:
            return DMChannel(data)
        
        elif self.type == 2:
            return GuildVoiceChannel(client, data)
        
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