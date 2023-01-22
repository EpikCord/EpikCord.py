
import aiohttp

class GatewayWebsocket(aiohttp.ClientWebSocketResponse):
    """A websocket connection to the Discord gateway."""
    ...