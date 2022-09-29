from __future__ import annotations

import datetime
from typing import TYPE_CHECKING, List, Optional

from .abstract import Messageable
from .exceptions import NotFound404, ThreadArchived

if TYPE_CHECKING:
    import discord_typings


class ThreadMember:
    def __init__(self, data: discord_typings.ThreadMemberData):
        self.id: int = int(data["user_id"])
        self.thread_id: int = int(data["id"])
        self.join_timestamp: datetime.datetime = datetime.datetime.fromisoformat(
            data["join_timestamp"]
        )
        self.flags: int = data["flags"] # Currently I don't know what the Flag is, so it's int for now.

class ThreadMetaData:
    def __init__(self, data: discord_typings.ThreadMetadata):
        self.archived: bool = data["archived"]
        self.auto_archive_duration: int = data["auto_archive_duration"]
        self.archive_timestamp: datetime.datetime = datetime.datetime.fromisoformat(
            data["archive_timestamp"]
        )
        self.locked: bool = data["locked"]
        self.invitable: Optional[bool] = data.get("invitable")
        self.create_timestamp: Optional[datetime.datetime] = datetime.datetime.fromisoformat(
            data["create_timestamp"]
        ) if data.get("create_timestamp") else None

class Thread(Messageable):
    def __init__(self, client, data: discord_typings.ThreadChannelData):
        super().__init__(client, int(data["id"]))
        
        self.owner_id: int = int(data["owner_id"])
        self.message_count: Optional[int] = data.get("message_count")
        self.member_count: Optional[int] = data.get("member_count")
        self.metadata: ThreadMetaData = ThreadMetaData(data["thread_metadata"])

    async def join(self):
        if self.archived:
            raise ThreadArchived(
                "This thread has been archived so it is no longer joinable"
            )
        await self.client.http.put(
            f"/channels/{self.id}/thread-members/@me", channel_id=self.id
        )

    async def add_member(self, member_id: str):
        if self.metadata.archived:
            raise ThreadArchived(
                "This thread has been archived so it is no longer joinable"
            )
        
        response = await self.client.http.put(
            f"/channels/{self.id}/thread-members/{member_id}", channel_id=self.id
        )
        return await response.json()

    async def leave(self):
        if self.archived:
            raise ThreadArchived(
                "This thread has been archived so it is no longer leaveable"
            )
        response = await self.client.http.delete(
            f"/channels/{self.id}/thread-members/@me", channel_id=self.id
        )
        return await response.json()

    async def remove_member(self, member_id: str):
        if self.metadata.archived:
            raise ThreadArchived(
                "This thread has been archived so it is no longer leaveable"
            )

        response = await self.client.http.delete(
            f"/channels/{self.id}/thread-members/{member_id}", channel_id=self.id
        )
        return await response.json()

    async def fetch_member(self, member_id: str) -> ThreadMember:
        from EpikCord import ThreadMember

        response = await self.client.http.get(
            f"/channels/{self.id}/thread-members/{member_id}", channel_id=self.id
        )
        if response.status == 404:
            raise NotFound404("The member you are trying to fetch does not exist")
        return ThreadMember(await response.json())

    async def list_members(self) -> List[ThreadMember]:
        from EpikCord import ThreadMember

        response = await self.client.http.get(
            f"/channels/{self.id}/thread-members", channel_id=self.id
        )
        return [ThreadMember(member) for member in await response.json()]

    async def bulk_delete(self, message_ids: List[str], reason: Optional[str]) -> None:

        if reason:
            headers = self.client.http.headers.copy()
            headers["X-Audit-Log-Reason"] = reason

        response = await self.client.http.post(
            f"channels/{self.id}/messages/bulk-delete",
            data={"messages": message_ids},
            headers=headers,
            channel_id=self.id,
        )
        return await response.json()


__all__ = ("Thread", "ThreadMember")
