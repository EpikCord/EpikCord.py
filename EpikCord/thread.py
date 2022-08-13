from __future__ import annotations
from .exceptions import ThreadArchived, NotFound404
from .abstract import Messageable
from typing import List, Optional
import datetime


class ThreadMember:
    def __init__(self, data: dict):
        self.id: str = data.get("user_id")
        self.thread_id: str = data.get("thread_id")
        self.join_timestamp: datetime.datetime = datetime.datetime.fromisoformat(
            data["join_timestamp"]
        )
        self.flags: int = data.get("flags")


class Thread(Messageable):
    def __init__(self, client, data: dict):
        super().__init__(client, data)
        self.owner_id: str = data.get("owner_id")
        self.message_count: int = data.get("message_count")
        self.member_count: int = data.get("member_count")
        self.archived: bool = data.get("archived")
        self.auto_archive_duration: int = data.get("auto_archive_duration")
        self.archive_timestamp: Optional[datetime.datetime] = (
            datetime.datetime.fromisoformat(data.get("archive_timestamp"))
            if data.get("archive_timestamp")
            else None
        )
        self.locked: bool = data.get("locked")

    async def join(self):
        if self.archived:
            raise ThreadArchived(
                "This thread has been archived so it is no longer joinable"
            )
        response = await self.client.http.put(
            f"/channels/{self.id}/thread-members/@me", channel_id=self.id
        )
        return await response.json()

    async def add_member(self, member_id: str):
        if self.archived:
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
        if self.archived:
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
