from typing import List, Optional
from .type_enums import (
    AutoModKeywordPresetTypes,
    AutoModActionType,
    AutoModEventType,
    AutoModTriggerType,
)


class AutoModTriggerMetaData:
    def __init__(self, data: dict):
        self.keyword_filter: List[str] = data.get("keyword_filter")
        self.presets: List[AutoModKeywordPresetTypes] = [
            AutoModKeywordPresetTypes(x) for x in data.get("presets")
        ]

    def to_dict(self):
        return {
            "keyword_filter": self.keyword_filter,
            "presets": [int(preset) for preset in self.presets],
        }

class AutoModActionMetaData:
    def __init__(self, data: dict):
        self.channel_id: str = data.get("channel_id")
        self.duration_seconds: int = data.get("duration_seconds")

    def to_dict(self):
        return {
            "channel_id": self.channel_id,
            "duration_seconds": self.duration_seconds,
        }

class AutoModAction:
    def __init__(self, data: dict):
        self.type: int = AutoModActionType(data["type"])
        self.metadata = AutoModActionMetaData(data["metadata"])

    def to_dict(self):
        return {
            "type": int(self.type),
            "metadata": self.metadata.to_dict(),
        }

class AutoModRule:
    def __init__(self, client, data: dict):
        self.client = client
        self.id: str = data["id"]
        self.guild_id: str = data["guild_id"]
        self.name: str = data["name"]
        self.creator_id: str = data["creator_id"]
        self.event_type = AutoModEventType(data["event_type"])
        self.trigger_type = AutoModTriggerType(data["trigger_type"])
        self.trigger_metadata: AutoModTriggerMetaData = [
            AutoModTriggerMetaData(data) for data in data["trigger_metadata"]
        ]
        self.actions: List[AutoModAction] = [
            AutoModAction(data) for data in data.get("actions")
        ]
        self.enabled: bool = data["enabled"]
        self.except_roles_ids: List[str] = data["except_roles"]
        self.except_channels_ids: List[str] = data["except_channels"]

    async def edit(
        self,
        *,
        name: Optional[str] = None,
        event_type: Optional[int] = None,
        trigger_metadata: Optional[AutoModTriggerMetaData] = None,
        actions: Optional[List[AutoModAction]] = None,
        enabled: Optional[bool] = None,
        exempt_roles: Optional[List[str]] = None,
        exempt_channels: Optional[List[str]] = None,
    ):
        payload = {}

        if name:
            payload["name"] = name

        if event_type:
            payload["event_type"] = int(event_type)

        if enabled is not None:
            payload["enabled"] = enabled

        if exempt_channels:
            payload["exempt_channels"] = exempt_channels

        if exempt_roles:
            payload["exempt_roles"] = exempt_roles

        if trigger_metadata is not None:
            payload["trigger_metadata"] = trigger_metadata.to_dict()

        if actions:
            payload["actions"] = [action.to_dict() for action in actions]

        await self.client.http.patch(
            f"/guilds/{self.guild_id}/auto-moderation/rules/{self.id}", json=payload
        )

    async def delete(self):
        await self.client.http.delete(
            f"guilds/{self.guild_id}/auto-moderation/rules/{self.id}"
        )

__all__ = ("AutoModTriggerMetaData", "AutoModActionMetaData", "AutoModAction", "AutoModRule")
