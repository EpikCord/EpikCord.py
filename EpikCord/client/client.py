from __future__ import annotations
from importlib.util import find_spec, module_from_spec, resolve_name
from sys import modules
from .websocket_client import WebsocketClient
from logging import getLogger
from importlib import import_module
from ..managers import ChannelManager, GuildManager
from ..sticker import Sticker, StickerPack
from collections import deque
from typing import Optional, List, Any, TYPE_CHECKING, Union
from ..flags import Intents

if TYPE_CHECKING:
    from EpikCord import Status, Activity, Section, Presence

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
        from EpikCord import Presence, ClientUser, ClientApplication, Utils

        self.overwrite_commands_on_ready: bool = overwrite_commands_on_ready or False
        self.guilds: GuildManager = GuildManager(self)
        self.channels: ChannelManager = ChannelManager(self)
        self.presence: Presence = Presence(status=status, activity=activity)
        self._components = {}
        self.utils = Utils(self)
        self.latencies = deque(maxlen=5)
        self.user: ClientUser = None
        self.application: Optional[ClientApplication] = None
        self.sections: List[Any] = []

    @property
    def latency(self):
        return self.discord_latency

    @property
    def average_latency(self):
        return sum(self.latencies) / len(self.latencies)

    def load_section(self, section: Section):

        for event in section._events.values():
            self.events[event.name] = event.callback

        for command in section._commands.values():
            self.commands[command.name] = command

    def load_sections_from_file(self, filename: str, *, package: str = None):
        name = resolve_name(filename, package)
        spec = find_spec(name)

        if not spec:
            raise ImportError(f"Could not find module {name}")
        sections_spec = module_from_spec(spec)

        try:
            spec.loader.exec_module(sections_spec)
        except Exception as e:
            raise ImportError(f"Could not load module {name}") from e

        sections = import_module(filename, package)

        modules[filename] = sections_spec

        from EpikCord import Section

        for possible_section in sections.__dict__.values():
            if issubclass(possible_section, Section):
                self.load_section(possible_section)

    async def fetch_sticker(self, sticker_id: str) -> Sticker:
        response = await self.http.get(f"/stickers/{sticker_id}")
        json = await response.json()
        return Sticker(self, json)  # TODO: Possibly cache this?

    async def list_nitro_sticker_packs(self) -> List[StickerPack]:
        response = await self.http.get("/sticker-packs")
        json = await response.json()
        return [StickerPack(self, pack) for pack in json["sticker_packs"]]

__all__ = ("Client",)
