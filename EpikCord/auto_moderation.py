from __future__ import annotations

from typing import Dict, List, Optional, TypedDict, Union, TYPE_CHECKING

from typing_extensions import NotRequired

from .type_enums import (
    AutoModActionType,
    AutoModEventType,
    AutoModKeywordPresetType,
    AutoModTriggerType,
)

if TYPE_CHECKING:
    import discord_typings

class AutoModTriggerMetadata:
    def __init__(self, data: discord_typings.AutoModerationTriggerMetadataData):
        self.keyword_filter: Optional[List[str]] = data["keyword_filter"] if data.get("keyword_filter") else None
        self.presets: Optional[List[AutoModKeywordPresetType]] = [
            AutoModKeywordPresetType(x) for x in data["presets"]
        ] if data.get("presets") else None

    def to_dict(self):
        return {
            "keyword_filter": self.keyword_filter,
            "presets": [int(preset) for preset in self.presets],
        }


class AutoModActionMetadata:
    def __init__(self, data: discord_typings.AutoModerationActionData):
        self.channel_id: int = int(data["channel_id"])
        self.duration_seconds: int = data["duration_seconds"]

    def to_dict(self):
        return {
            "channel_id": self.channel_id,
            "duration_seconds": self.duration_seconds,
        }


class AutoModAction:
    def __init__(self, data: discord_typings.AutoModerationActionData):
        self.type: int = AutoModActionType(data["type"])
        self.metadata = AutoModActionMetaData(data["metadata"])

    def to_dict(self):
        return {
            "type": int(self.type),
            "metadata": self.metadata.to_dict(),
        }


class AutoModRulePayload(TypedDict):
    name: NotRequired[str]
    event_type: NotRequired[discord_typings.AutoModerationEventTypes]
    trigger_metadata: NotRequired[discord_typings.AutoModerationTriggerMetadataData]
    actions: NotRequired[List[discord_typings.AutoModerationActionData]]
    enabled: NotRequired[bool]
    exempt_roles: NotRequired[List[int]]
    exempt_channels: NotRequired[List[int]]


class AutoModRule:
    def __init__(self, client, data: discord_typings.AutoModerationRuleData):
        self.client = client
        self.id: int = int(data["id"])
        self.guild_id: int = int(data["guild_id"])
        self.name: str = data["name"]
        self.creator_id: int = int(data["creator_id"])
        self.event_type = AutoModEventType(data["event_type"])
        self.trigger_type: Optional[AutoModTriggerType] = AutoModTriggerType(data["trigger_type"]) if data.get("trigger_type") else None
        self.trigger_metadata: List[AutoModTriggerMetadata] = [
            AutoModTriggerMetadata(d) for d in data["trigger_metadata"]
        ]
        self.actions: List[AutoModAction] = [
            AutoModAction(data) for data in data["actions"]
        ]
        self.enabled: bool = data["enabled"]
        self.except_roles_ids: List[int] = [int(role) for role in data["except_roles"]] if data.get("except_roles") else []
        self.except_channels_ids: List[int] = [int(channel) for channel in data["except_channels"]] if data.get("except_channels") else []

    async def edit(
        self,
        *,
        name: Optional[str] = None,
        event_type: Optional[discord_typings.AutoModerationEventTypes] = None,
        trigger_metadata: Optional[AutoModTriggerMetadata] = None,
        actions: Optional[List[AutoModAction]] = None,
        enabled: Optional[bool] = None,
        exempt_roles: Optional[List[int]] = None,
        exempt_channels: Optional[List[int]] = None,
    ):
        payload: AutoModRulePayload = {}

        if name:
            payload["name"] = name

        if event_type:
            payload["event_type"] = event_type

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


__all__ = (
    "AutoModTriggerMetadata",
    "AutoModActionMetadata",
    "AutoModAction",
    "AutoModRule",
)
