from __future__ import annotations

from logging import getLogger
from typing import TYPE_CHECKING, Any, Callable, Coroutine, Dict, List, Optional, Union

from ..flags import Intents
from ..sticker import Sticker, StickerPack
from .command_handler import CommandHandler
from .websocket_client import WebsocketClient

if TYPE_CHECKING:
    import discord_typings

    from EpikCord import Presence, Section

logger = getLogger(__name__)

Callback = Callable[..., Coroutine[Any, Any, Any]]


class Client(WebsocketClient, CommandHandler):
    def __init__(
        self,
        token: str,
        intents: Union[Intents, int] = 0,
        *,
        overwrite_commands_on_ready: bool = False,
        discord_endpoint: str = "https://discord.com/api/v10",
        presence: Optional[Presence] = None,
    ):
        super().__init__(token, intents, presence, discord_endpoint=discord_endpoint)
        CommandHandler.__init__(self)
        from EpikCord import Utils

        self.overwrite_commands_on_ready: bool = overwrite_commands_on_ready or False
        self._components: Dict[str, Callback] = {}
        self.utils = Utils(self)

        self.sections: List[Section] = []

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

    async def _interaction_create(self, data: discord_typings.InteractionCreateEvent):
        await super()._interaction_create(data)
        interaction = self.utils.interaction_from_type(data)
        await self.handle_interaction(interaction)


    def component(self, custom_id: str):
        def wrapper(func):
            self._components[custom_id] = func
            return func
        return wrapper

__all__ = ("Client",)
