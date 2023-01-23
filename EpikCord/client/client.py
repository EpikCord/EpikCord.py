from ..flags import Intents
from .http import HTTPClient, APIVersion

def singleton(cls):
    instance = None

    def wrapper(*args, **kwargs):
        nonlocal instance

        if instance is None:
            instance = cls(*args, **kwargs)
        return instance

    return wrapper


@singleton
class TokenStore:

    def __init__(self, token: str):
        self.value: str = token

class Client:
    """The main class of EpikCord. Use this to interact with the Discord API and Gateway."""

    def __init__(self, token: TokenStore, intents: Intents, *, version: APIVersion = APIVersion.TEN):
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
        self.token: TokenStore = token
        self.intents: Intents = intents
        self.http: HTTPClient = HTTPClient(token, version=version)
