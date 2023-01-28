import asyncio
from typing import Optional

from ..flags import Intents
from ..presence import Presence
from ..utils import cleanup_loop, singleton
from .http import APIVersion, HTTPClient
from .websocket import WebSocketClient


@singleton
class TokenStore:
    def __init__(self, token: str):
        self.value: str = token


class Client(WebSocketClient):
    """
    The main class of EpikCord.
    Use this to interact with the Discord API and Gateway.
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

        Attributes
        ----------
        token: str
            The token of the bot.
        intents: Intents
            The intents of the bot.
        http: HTTPClient
            The HTTP client used to interact with the Discord API.
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
