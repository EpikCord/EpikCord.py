import asyncio
from logging import getLogger
from typing import List, Optional, Union

from ..flags import Intents, Permissions
from ..locales import Localization
from ..presence import Presence
from ..types import OpCode
from ..utils import AsyncFunction, cleanup_loop, singleton
from .commands import (
    ApplicationCommandOption,
    ApplicationCommandType,
    ClientChatInputCommand,
    ClientMessageCommand,
    ClientUserCommand,
)
from .http import APIVersion, HTTPClient
from .websocket import WebSocketClient

logger = getLogger("EpikCord.client")


@singleton
class TokenStore:
    def __init__(self, token: str):
        self.value: str = token

    def remove_from(self, string: str) -> str:
        return string.replace(self.value, "[REMOVED TOKEN]")


class Client(WebSocketClient):
    """
    The main class of EpikCord.
    Use this to interact with the Discord API and Gateway.

    Attributes
    ----------
    token: str
        The token of the bot.
    intents: Intents
        The intents of the bot.
    http: HTTPClient
        The HTTP client used to interact with the Discord API.
    """

    def __init__(
        self,
        token: TokenStore,
        intents: Intents,
        *,
        version: APIVersion = APIVersion.TEN,
        presence: Optional[Presence] = None,
    ):
        """
        Parameters
        ----------
        token: str
            The token of the bot.
        intents: Intents
            The intents of the bot.
        version: int
            The version of the Discord API to use. Defaults to 10.
        """
        super().__init__(
            token,
            intents,
            presence=presence,
            http=HTTPClient(token, version=version),
        )
        self.commands: List[
            Union[ClientChatInputCommand, ClientUserCommand, ClientMessageCommand]
        ] = []

    def login(self):
        loop = asyncio.get_event_loop()

        async def runner():
            try:
                await self.connect()
            finally:
                logger.critical("Final clause triggered.")
                await self.close()

        def stop_loop_on_completion(f: asyncio.Future):
            loop.stop()

        future = asyncio.ensure_future(runner(), loop=loop)
        future.add_done_callback(stop_loop_on_completion)

        try:
            loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            future.remove_done_callback(stop_loop_on_completion)
            cleanup_loop(loop)

    async def close(self):
        logger.critical("Closing connections")

        if self.ws and not self.ws.closed:
            if self._heartbeat_task:
                self._heartbeat_task.cancel()
                self._heartbeat_task = None
            await self.ws.close()

        if not self.http.session.closed:
            await self.http.session.close()

        self.rate_limiter.reset.cancel()

    async def change_presence(self, presence: Presence):
        if not self.ws:
            raise RuntimeError("Client is not connected to the gateway.")
        await self.ws.send_json({"op": OpCode.PRESENCE_UPDATE, "d": presence.to_dict()})

    def command(
        self,
        name: str,
        description: str,
        *,
        guild_ids: Optional[List[int]] = None,
        name_localizations: Optional[List[Localization]] = None,
        description_localizations: Optional[List[Localization]] = None,
        guild_only: Optional[bool] = None,
        default_member_permissions: Optional[Permissions] = None,
        options: Optional[List[ApplicationCommandOption]] = None,
        nsfw: bool = False,
    ):  # TODO: Add in types for command callbacks
        def wrapper(func: AsyncFunction):
            command = ClientChatInputCommand(
                name,
                description,
                func,
                guild_ids=guild_ids,
                name_localizations=name_localizations,
                description_localizations=description_localizations,
                type=ApplicationCommandType.CHAT_INPUT,
                guild_only=guild_only,
                default_member_permissions=default_member_permissions,
                nsfw=nsfw,
                options=options,
            )
            self.commands.append(command)
            return command

        return wrapper
