from ..flags import Intents


class Client:
    def __init__(self, token: str, intents: Intents):
        self.token: str = token
        self.intents: Intents = intents
