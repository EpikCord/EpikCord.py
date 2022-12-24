from ..flags import Intents
from .http import HTTPClient


class Client:
    def __init__(self, token: str, intents: Intents, *, version: int = 10):
        self.token: str = token
        self.intents: Intents = intents
        self.http: HTTPClient = HTTPClient(token, version=version)
