from typing import Dict, List, Optional, TypedDict, Union
from typing_extensions import NotRequired

import discord_typings

from .type_enums import (
    AutoModActionType,
    AutoModEventType,
    AutoModKeywordPresetType,
    AutoModTriggerType,
)


class AutoModTriggerMetaData:
    def __init__(self, data: dict):
        self.keyword_filter: List[str] = data["keyword_filter"]
        self.presets: List[AutoModKeywordPresetType] = [
            AutoModKeywordPresetType(x) for x in data["presets"]
        ]

    def to_dict(self):
        return {
            "keyword_filter": self.keyword_filter,
            "presets": [int(preset) for preset in self.presets],
        }


class AutoModActionMetaData:
    def __init__(self, data: dict):
        self.channel_id: int = int(data["channel_id"])
        self.duration_seconds: int = data["duration_seconds"]

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

class AutoModRulePayload(TypedDict):
    name: NotRequired[str]
    event_type: NotRequired[discord_typings.AutoModerationEventTypes]
    trigger_metadata: NotRequired[discord_typings.AutoModerationTriggerMetadataData]
    actions: NotRequired[List[discord_typings.AutoModerationActionData]]
    enabled: NotRequired[bool]
    exempt_roles: NotRequired[List[int]]
    exempt_channels: NotRequired[List[int]]


class AutoModRule:
    def __init__(self, client, data: dict):
        self.client = client
        self.id: str = data["id"]
        self.guild_id: str = data["guild_id"]
        self.name: str = data["name"]
        self.creator_id: str = data["creator_id"]
        self.event_type = AutoModEventType(data["event_type"])
        self.trigger_type = AutoModTriggerType(data["trigger_type"])
        self.trigger_metadata: List[AutoModTriggerMetaData] = [
            AutoModTriggerMetaData(data) for data in data["trigger_metadata"]
        ]
        self.actions: List[AutoModAction] = [
            AutoModAction(data) for data in data["actions"]
        ]
        self.enabled: bool = data["enabled"]
        self.except_roles_ids: List[str] = data["except_roles"]
        self.except_channels_ids: List[str] = data["except_channels"]

    async def edit(
        self,
        *,
        name: Optional[str] = None,
        event_type: Optional[discord_typings.AutoModerationEventTypes] = None,
        trigger_metadata: Optional[AutoModTriggerMetaData] = None,
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
    "AutoModTriggerMetaData",
    "AutoModActionMetaData",
    "AutoModAction",
    "AutoModRule",
)
