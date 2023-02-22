import asyncio
from typing import Optional

from ..flags import Intents
from ..presence import Presence
from ..utils import OpCode, cleanup_loop, singleton, AsyncFunction
from .http import APIVersion, HTTPClient
from .websocket import WebSocketClient


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

    def login(self):
        loop = asyncio.get_event_loop()

        async def runner():
            try:
                await self.connect()
            finally:
                if not self.http.session.closed:
                    await self.http.close()

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
        if not self.http.session.closed:
            await self.http.session.close()

        if self.ws and self.ws.closed:
            await self.ws.close()

        self.rate_limiter.reset.cancel()

    async def change_presence(self, presence: Presence):
        if not self.ws:
            raise RuntimeError("Client is not connected to the gateway.")
        await self.ws.send_json(
            {"op": OpCode.PRESENCE_UPDATE, "d": presence.to_dict()}
        )

    def command(
        self, function: AsyncFunction
    ):  # TODO: Add in types for command callbacks
        ...
