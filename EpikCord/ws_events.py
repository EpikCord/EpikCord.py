from __future__ import annotations

from functools import partial
from typing import TYPE_CHECKING, Callable, Dict

from .opcodes import GatewayOpcode

if TYPE_CHECKING:
    from .client import WebsocketClient


class WSEHandler:
    @staticmethod
    async def dispatch(ws_client, event_data):
        ws_client.sequence = event_data["s"]
        await ws_client.handle_event(event_data["t"].lower(), event_data["d"])

    @staticmethod
    async def heartbeat(ws_client, _event_data):
        await ws_client.heartbeat(True)

    @staticmethod
    async def reconnect(ws_client, _event_data):
        await ws_client.reconnect()
        await ws_client.resume()

    @staticmethod
    async def invalid_session(ws_client, event_data):
        if event_data["d"]:
            await ws_client.reconnect()
            await ws_client.resume()
            return

        await ws_client.reconnect()

    @staticmethod
    async def hello(ws_client, event_data):
        ws_client.heartbeat_interval = event_data["d"]["heartbeat_interval"] / 1000
        await ws_client.identify()

    @staticmethod
    def heartbeat_ack(ws_client, event_data):
        ws_client.heartbeats.append(event_data)


# TODO: replace Dict with discord typing
WSEHandlerMapping = Dict[GatewayOpcode, Callable[[Dict], None]]


def setup_ws_event_handler(ws_client: WebsocketClient) -> WSEHandlerMapping:
    return {
        g_opcode: partial(method, ws_client)
        for g_opcode, method in (
            (GatewayOpcode.DISPATCH, WSEHandler.dispatch),
            (GatewayOpcode.HEARTBEAT, WSEHandler.heartbeat),
            (GatewayOpcode.RECONNECT, WSEHandler.reconnect),
            (GatewayOpcode.INVALID_SESSION, WSEHandler.invalid_session),
            (GatewayOpcode.HELLO, WSEHandler.hello),
            (GatewayOpcode.HEARTBEAT_ACK, WSEHandler.heartbeat_ack),
        )
    }
