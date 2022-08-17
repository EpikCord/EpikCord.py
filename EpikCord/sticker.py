from typing import Optional, List
from .type_enums import StickerFormatType, StickerType
from .user import User


class StickerItem:
    def __init__(self, data: dict):
        self.id: str = data["id"]
        self.name: str = data["name"]
        self.format_type: StickerFormatType = StickerFormatType(data["format_type"])


class Sticker:
    def __init__(self, client, data: dict):
        self.client = client
        self.id: int = int(data["id"])
        self.pack_id: Optional[int] = (
            int(data["pack_id"]) if data.get("pack_id") else None
        )
        self.name: str = data["name"]
        self.description: Optional[str] = data.get("description")
        self.tags: List[str] = data["tags"].split(",")
        self.type: StickerType = StickerType(data["type"])
        self.format_type: StickerFormatType = StickerFormatType(data["format_type"])
        self.available: Optional[bool] = data.get("available")
        self.guild_id: Optional[int] = data.get("guild_id")
        self.user: Optional[User] = (
            User(self.client, data["user"]) if data.get("user") else None
        )
        self.sort_value: Optional[int] = data.get("sort_value")

    async def edit(
        self,
        *,
        name: Optional[str] = None,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
    ):
        if not self.guild_id:
            raise ValueError("Cannot edit a sticker that is not in a guild.")
        payload = {}
        if name:
            payload["name"] = name
        if description:
            payload["description"] = description
        if tags:
            payload["tags"] = ",".join(tags)
        await self.client.http.patch(
            f"/guilds/{self.guild_id}/stickers/{self.id}",
            json=payload,
            guild_id=self.guild_id,
        )
        return

    async def delete(self, reason: Optional[str]):
        if not self.guild_id:
            raise ValueError("Cannot delete a sticker that is not in a guild.")
        headers = self.client.headers.copy()
        if reason:
            headers["X-Audit-Log-Reason"] = reason
        await self.client.http.delete(
            f"/guilds/{self.guild_id}/stickers/{self.id}",
            headers=headers,
            guild_id=self.guild_id,
        )
        return


class StickerPack:
    def __init__(self, client, data: dict):
        self.client = client
        self.id: int = int(data["id"])
        self.stickers: List[Sticker] = [
            Sticker(self.client, s) for s in data["stickers"]
        ]
        self.name: str = data["name"]
        self.sku_id: int = int(data["sku_id"])
        self.cover_sticker_id: Optional[int] = (
            int(data["cover_sticker_id"]) if data.get("cover_sticker_id") else None
        )
        self.description: str = data["description"]
        self.banner_asset_id: Optional[int] = (
            int(data["banner_asset_id"]) if data.get("banner_asset_id") else None
        )


__all__ = ("StickerItem", "Sticker")
