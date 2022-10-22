from typing import Optional

from aiohttp import ClientSession


class WebhookClient:
    def __init__(self, url: str, session: ClientSession = ClientSession()):
        self.url: str = url
        self.session = session

    # async def send(self, *, content: Optional[str] = None, username: Optional[str] = None, avatar_url: Optional[str] = None, tts: bool = False, )
