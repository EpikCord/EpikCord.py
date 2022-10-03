from __future__ import annotations

from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from ..client.client import Client, WebsocketClient

from .cache_manager import CacheManager


class MemberManager(CacheManager):
    def __init__(self, client: Union[Client, WebsocketClient], guild_id: int):
        super().__init__()
        self.client = client
        self.guild_id: int = guild_id
