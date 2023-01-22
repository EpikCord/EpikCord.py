from ..flags import Intents
from .http import HTTPClient


class Client:
    """The main class of EpikCord. Use this to interact with the Discord API and Gateway."""
    def __init__(self, token: str, intents: Intents, *, version: int = 10):
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
        self.token: str = token
        self.intents: Intents = intents
        self.http: HTTPClient = HTTPClient(token, version=version)
