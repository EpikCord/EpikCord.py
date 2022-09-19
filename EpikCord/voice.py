from __future__ import annotations
import datetime
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    import discord_typings

class VoiceRegion:
    def __init__(self, data: discord_typings.VoiceRegionData):
        self.id: str = data["id"]
        self.name: str = data["name"]
        self.optimal: bool = data["optimal"]
        self.deprecated: bool = data["deprecated"]
        self.custom: bool = data["custom"]


class VoiceState:
    def __init__(self, client, data: discord_typings.VoiceStateData):
        from EpikCord import GuildMember

        self.data = data
        self.guild_id: Optional[int] = int(data["guild_id"]) if data.get("guild_id") else None
        self.channel_id: int = int(data["channel_id"]) # type: ignore
        self.user_id: int = int(data["user_id"])
        self.member: Optional[GuildMember] = (
            GuildMember(client, data["member"]) if data.get("member") else None
        )
        self.session_id: str = data["session_id"]
        self.deaf: bool = data["deaf"]
        self.mute: bool = data["mute"]
        self.self_deaf: bool = data["self_deaf"]
        self.self_mute: bool = data["self_mute"]
        self.self_stream: Optional[bool] = data.get("self_stream")
        self.self_video: bool = data["self_video"]
        self.suppress: bool = data["suppress"]
        self.request_to_speak_timestamp: Optional[datetime.datetime] = (
            datetime.datetime.fromisoformat(data["request_to_speak_timestamp"])  # type: ignore
            if data.get("request_to_speak_timestamp")
            else None
        )


__all__ = ("VoiceRegion", "VoiceState")
