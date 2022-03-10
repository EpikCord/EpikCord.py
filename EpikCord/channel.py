from .message import Message, Messageable
from .member import PartialUser
from .thread import Thread, ThreadMember
from typing import Optional, List, Dict, Union


class Overwrite:
    def __init__(self, data: dict):
        self.id: str = data.get("id")
        self.type: int = data.get("type")
        self.allow: str = data.get("allow")
        self.deny: str = data.get("deny")

class BaseChannel:
    def __init__(self, client, data: dict):
        self.id: str = data.get("id")
        self.client = client
        self.type = data.get("type")


class WelcomeScreenChannel:
    def __init__(self, data: dict):
        self.channel_id: str = data.get("channel_id")
        self.description: str = data.get("description")
        self.emoji_id: Optional[str] = data.get("emoji_id")
        self.emoji_name: Optional[str] = data.get("emoji_name")

class WelcomeScreen:
    def __init__(self, data: dict):
        self.description: Optional[str] = data.get("description")
        self.welcome_channels: List[WelcomeScreenChannel] = [WelcomeScreenChannel(welcome_channel) for welcome_channel in data.get("welcome_channels")]

class GuildChannel(BaseChannel):
    def __init__(self, client, data: dict):
        super().__init__(client, data)
        if data["type"] == 0:
            return TextBasedChannel(client, data).to_type()
        self.guild_id: str = data.get("guild_id")
        self.position: int = data.get("position")
        self.nsfw: bool = data.get("nsfw")
        self.permission_overwrites: List[dict] = data.get(
            "permission_overwrites")
        self.parent_id: str = data.get("parent_id")
        self.name: str = data.get("name")

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
        return [Message(self.client, message) for message in data]

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
        self.topic: str = data.get("topic")
        self.rate_limit_per_user: int = data.get("rate_limit_per_user")
        self.last_message_id: str = data.get("last_message_id")
        self.default_auto_archive_duration: int = data.get(
            "default_auto_archive_duration")

    async def create_webhook(self, *, name: str, avatar: Optional[str] = None, reason: Optional[str] = None):
        headers = self.client.http.headers.clone()
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


class VoiceChannel(GuildChannel):
    def __init__(self, client, data: dict):
        super().__init__(client, data)
        self.bitrate: int = data.get("bitrate")
        self.user_limit: int = data.get("user_limit")
        self.rtc_region: str = data.get("rtc_region")


class DMChannel(BaseChannel):
    def __init__(self, client, data: dict):
        super().__init__(client, data)
        self.recipient: List[PartialUser] = PartialUser(data.get("recipient"))


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
        self.guild_id: str = data.get("guild_id")
        self.channel_id: str = data.get("channel_id")
        self.privacy_level: int = data.get("privacy_level")
        self.discoverable_disabled: bool = data.get("discoverable_disabled")

def _figure_out_channel_type(client, channel):
    channel_type = channel["type"]
    if channel_type == 0:
        return GuildTextChannel(client, channel)
    elif channel_type == 1:
        return DMChannel(client, channel)
    elif channel_type == 2:
        return VoiceChannel(client, channel)
    elif channel_type == 4:
        return ChannelCategory(client, channel)
    elif channel_type == 5:
        return GuildNewsChannel(client, channel)
    elif channel_type == 6:
        return GuildStoreChannel(client, channel)
    elif channel_type == 10:
        return GuildNewsThread(client, channel)
    elif  channel_type in (11, 12):
        return Thread(client, channel)
    elif channel_type == 13:
        return GuildStageChannel(client, channel)

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

        elif self.type == 11 or self.type == 12:
            return Thread(self.client, self.data)

        elif self.type == 13:
            return GuildStageChannel(self.client, self.data)


class SourceChannel:
    def __init__(self, data: dict):
        self.id: str = data.get("id")
        self.name: str = data.get("name")

class MentionedChannel:
    def __init__(self, data: dict):
        self.id: str = data.get("id")
        self.guild_id: str = data.get("guild_id")
        self.type: int = data.get("type")
        self.name: str = data.get("name")
