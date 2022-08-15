import datetime
from typing import Optional


class VoiceRegion:
    def __init__(self, data: dict):
        self.id: str = data["id"]
        self.name: str = data["name"]
        self.optimal: bool = data["optimal"]
        self.deprecated: bool = data["deprecated"]
        self.custom: bool = data["custom"]


class VoiceState:
    def __init__(self, client, data: dict):
        from EpikCord import GuildMember

        self.data: dict = data
        self.guild_id: Optional[str] = data.get("guild_id")
        self.channel_id: str = data["channel_id"]
        self.user_id: str = data["user_id"]
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
            datetime.datetime.fromisoformat(data["request_to_speak_timestamp"])
            if data.get("request_to_speak_timestamp")
            else None
        )


__all__ = ("VoiceRegion", "VoiceState")
