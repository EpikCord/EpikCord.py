from typing import (
    List
)
from .channels import GuildTextChannel
from .exceptions import ThreadArchived, NotFound404

class ThreadMember:
    def __init__(self, data: dict):
        self.thread_id: str = data["thread_id"]
        self.user_id: str = data["user_id"]
        self.join_timestamp: str = data["join_timestamp"]
        self.flags: int = data["flags"]

class Thread(GuildTextChannel):
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