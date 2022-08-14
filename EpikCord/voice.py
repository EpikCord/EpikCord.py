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
        self.channel_id: str = data.get("channel_id")
        self.user_id: str = data.get("user_id")
        self.member: Optional[GuildMember] = (
            GuildMember(client, data.get("member")) if data.get("member") else None
        )
        self.session_id: str = data.get("session_id")
        self.deaf: bool = data.get("deaf")
        self.mute: bool = data.get("mute")
        self.self_deaf: bool = data.get("self_deaf")
        self.self_mute: bool = data.get("self_mute")
        self.self_stream: Optional[bool] = data.get("self_stream")
        self.self_video: bool = data.get("self_video")
        self.suppress: bool = data.get("suppress")
        self.request_to_speak_timestamp: Optional[datetime.datetime] = (
            datetime.datetime.fromisoformat(data.get("request_to_speak_timestamp"))
            if data.get("request_to_speak_timestamp")
            else None
        )


__all__ = ("VoiceRegion", "VoiceState")
