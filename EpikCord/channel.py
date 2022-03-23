from typing import Optional, List, Dict, Union
#from .__init__ import GuildChannel, Messageable, Thread, PartialUser
from aiohttp import *
from .thread import *

class BaseChannel:
    def __init__(self, client, data: dict):
        self.id: str = data.get("id")
        self.client = client
        self.type = data.get("type")

class ChannelCategory(GuildChannel):
    def __init__(self, client, data: dict):
        super().__init__(client, data)

class GuildTextChannel(GuildChannel, Messageable):
    def __init__(self, client, data: dict):
        super().__init__(client, data)
        self.topic: str = data.get("topic")
        self.rate_limit_per_user: int = data.get("rate_limit_per_user")
        self.last_message_id: str = data.get("last_message_id")
        self.default_auto_archive_duration: int = data.get(
            "default_auto_archive_duration")

    async def create_webhook(self, *, name: str, avatar: Optional[str] = None, reason: Optional[str] = None):
        headers = client.http.headers.clone()
        if reason:
            headers["X-Audit-Log-Reason"] = reason

    async def start_thread(self, name: str, *, auto_archive_duration: Optional[int], type: Optional[int], invitable: Optional[bool], rate_limit_per_user: Optional[int], reason: Optional[str]):
        data = {"name": name}
        if auto_archive_duration:
            data["auto_archive_duration"] = auto_archive_duration
        if type:
            data["type"] = type
        if invitable is not None:  # Geez having a bool is gonna be a pain
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

    # It returns a List of Threads but I can't typehint that...
    async def list_public_archived_threads(self, *, before: Optional[str], limit: Optional[int]) -> Dict[str, Union[List[Messageable], List[ThreadMember], bool]]:
        response = await self.client.http.get(f"/channels/{self.id}/threads/archived/public", params={"before": before, "limit": limit})
        return await response.json()

    # It returns a List of Threads but I can't typehint that...
    async def list_private_archived_threads(self, *, before: Optional[str], limit: Optional[int]) -> Dict[str, Union[List[Messageable], List[ThreadMember], bool]]:
        response = await self.client.http.get(f"/channels/{self.id}/threads/archived/private", params={"before": before, "limit": limit})
        return await response.json()

    async def list_joined_private_archived_threads(self, *, before: Optional[str], limit: Optional[int]) -> Dict[str, Union[List[Messageable], List[ThreadMember], bool]]:
        response = await self.client.http.get(f"/channels/{self.id}/threads/archived/private", params={"before": before, "limit": limit})
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
        self.default_auto_archive_duration: int = data.get(
            "default_auto_archive_duration")

    async def follow(self, webhook_channel_id: str):
        response = await self.client.http.post(f"/channels/{self.id}/followers", data={"webhook_channel_id": webhook_channel_id})
        return await response.json()

class DMChannel(BaseChannel):
    def __init__(self, client, data: dict):
        super().__init__(client, data)
        self.recipient: List[PartialUser] = PartialUser(data.get("recipient"))

class GuildNewsThread(Thread, GuildNewsChannel):
    def __init__(self, client, data: dict):
        super().__init__(client, data)

class GuildStoreChannel(GuildChannel):
    def __init__(self, client, data: dict):
        super().__init__(client, data)

class GuildStageChannel(BaseChannel):
    def __init__(self, client, data: dict):
        super().__init__(client, data)
        self.guild_id: str = data.get("guild_id")
        self.channel_id: str = data.get("channel_id")
        self.privacy_level: int = data.get("privacy_level")
        self.discoverable_disabled: bool = data.get("discoverable_disabled")

class TextBasedChannel:
    def __init__(self, client, data: dict):
        self.client = client
        self.data: dict = data

    def to_type(self):
        if self.type == 0:
            return GuildTextChannel(self.client, self.data)

        elif self.type == 1:
            return DMChannel(self.client, self.data)

        elif self.type == 4:
            return ChannelCategory(self.client, self.data)

        elif self.type == 5:
            return GuildNewsChannel(self.client, self.data)

        elif self.type == 6:
            return GuildStoreChannel(self.client, self.data)

        elif self.type == 10:
            return GuildNewsThread(self.client, self.data)

        elif self.type in [11, 12]:
            return Thread(self.client, self.data)

        elif self.type == 13:
            return GuildStageChannel(self.client, self.data)