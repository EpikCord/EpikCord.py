from __future__ import annotations

from collections import deque
from logging import getLogger
from typing import TYPE_CHECKING, Any, List, Optional, Union

from ..flags import Intents
from ..managers import ChannelManager, GuildManager
from ..sticker import Sticker, StickerPack
from .websocket_client import WebsocketClient

if TYPE_CHECKING:
    from EpikCord import Activity, Presence, Section, Status

logger = getLogger(__name__)


class Client(WebsocketClient):
    def __init__(
        self,
        token: str,
        intents: Union[Intents, int] = 0,
        *,
        status: Optional[Status] = None,
        activity: Optional[Activity] = None,
        overwrite_commands_on_ready: Optional[bool] = None,
        discord_endpoint: str = "https://discord.com/api/v10",
        presence: Presence = None,
    ):
        super().__init__(token, intents, presence, discord_endpoint=discord_endpoint)
        from EpikCord import ClientApplication, ClientUser, Presence, Utils

        self.overwrite_commands_on_ready: bool = overwrite_commands_on_ready or False
        self.guilds: GuildManager = GuildManager(self)
        self.channels: ChannelManager = ChannelManager(self)
        self.presence: Presence = Presence(status=status, activity=activity)
        self._components = {}
        self.utils = Utils(self)
        self.latencies = deque(maxlen=5)
        self.user: Optional[ClientUser] = None
        self.application: Optional[ClientApplication] = None
        self.sections: List[Section] = []

    @property
    def latency(self):
        return self.discord_latency

    @property
    def average_latency(self):
        return sum(self.latencies) / len(self.latencies)

    def load_section(self, section_class: Section):
        section = section_class(self)  # type: ignore
        for event in section._events.values():
            self.events[event.name] = event.callback

        for command in section._commands.values():

            self.commands[command.name] = command

    async def fetch_sticker(self, sticker_id: str) -> Sticker:
        response = await self.http.get(f"/stickers/{sticker_id}")
        json = await response.json()
        return Sticker(self, json)  # TODO: Possibly cache this?

    async def list_nitro_sticker_packs(self) -> List[StickerPack]:
        response = await self.http.get("/sticker-packs")
        json = await response.json()
        return [StickerPack(self, pack) for pack in json["sticker_packs"]]


__all__ = ("Client",)
