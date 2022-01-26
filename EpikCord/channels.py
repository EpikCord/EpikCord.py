from .member import ThreadMember
from .exceptions import ThreadArchived, NotFound404
from .invite import Invite
from .client import Client
from .permissions import Overwrite
from .message import Message
from .partials import PartialUser
from .abc import BaseChannel
from typing import (
    List,
    Optional,
    Dict,
    Union
)

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
        response = await self.client.http.post(f"channels/{self.id}/messages", data=message_data)
        return Message(await response.json())


class GuildChannel(BaseChannel):
    def __init__(self, client: Client, data: dict):
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
            headers["reason"] = reason
            
        response = await self.client.http.delete(f"channels/{self.id}", headers=headers)
        return await response.json()
    
    async def fetch_invites(self) -> List[Invite]: 
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
        await self.client.http.post(f"/channels/{self.id}/invites", data=data)   
        
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
    def __init__(self, client: Client, data: dict):
        super().__init__(client, data)
        self.topic: str = data["topic"]
        self.rate_limit_per_user: int = data["rate_limit_per_user"]
        self.last_message_id: str = data["last_message_id"]
        self.default_auto_archive_duration: int = data["default_auto_archive_duration"]
    
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
        
        response = await self.client.http.post(f"channels/{self.id}/threads", data=data, headers=headers)
        self.client.guilds[self.guild_id].append(Thread(await response.json()))
    
    async def bulk_delete(self, message_ids: List[Message.id], reason: Optional[str]) -> None:

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
    def __init__(self, client: Client, data: dict):
        super().__init__(client, data)
        self.default_auto_archive_duration: int = data["default_auto_archive_duration"]

    async def follow(self, webhook_channel_id: str):
        response = await self.client.http.post(f"/channels/{self.id}/followers", data={"webhook_channel_id": webhook_channel_id})
        return await response.json()

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
        
class Thread(GuildTextChannel):
    def __init__(self, client: Client, data: dict):
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
    
    async def add_member(self, member_id: ThreadMember.id):
        if self.archived:
            raise ThreadArchived("This thread has been archived so it is no longer joinable")
        
        response = await self.client.http.put(f"/channels/{self.id}/thread-members/{member_id}")
        return await response.json()
    
    async def leave(self):
        if self.archived:
            raise ThreadArchived("This thread has been archived so it is no longer leaveable")
        response = await self.client.http.delete(f"/channels/{self.id}/thread-members/@me")
        return await response.json()
    
    async def remove_member(self, member_id: ThreadMember.id):
        if self.archived:
            raise ThreadArchived("This thread has been archived so it is no longer leaveable")
        
        response = await self.client.http.delete(f"/channels/{self.id}/thread-members/{member_id}")
        return await response.json()
    
    async def fetch_member(self, member_id: ThreadMember.user_id) -> ThreadMember:
        response = await self.client.http.get(f"/channels/{self.id}/thread-members/{member_id}")
        if response.status == 404:
            raise NotFound404("The member you are trying to fetch does not exist")
        return ThreadMember(await response.json())
    
    async def list_members(self) -> List[ThreadMember]:
        response = await self.client.http.get(f"/channels/{self.id}/thread-members")
        return [ThreadMember(member) for member in await response.json()]
            
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