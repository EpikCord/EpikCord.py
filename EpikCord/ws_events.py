from __future__ import annotations

from functools import partial
from typing import TYPE_CHECKING, Callable, Dict, Union

from .opcodes import GatewayOpcode

if TYPE_CHECKING:
    from .client import WebsocketClient


class WSEHandler:
    @staticmethod
    def dispatch(ws_client, event_data):
        ws_client.sequence = event_data["s"]
        await ws_client.handle_event(event_data["t"], event_data["d"])

    @staticmethod
    def heartbeat(ws_client, _event_data):
        await ws_client.heartbeat(True)

    @staticmethod
    def reconnect(ws_client, _event_data):
        await ws_client.reconnect()
        await ws_client.resume()

    @staticmethod
    def invalid_session(ws_client, event_data):
        if event_data["d"]:
            await ws_client.reconnect()
            await ws_client.resume()
            return

        await ws_client.reconnect()

    @staticmethod
    def hello(ws_client, event_data):
        ws_client.heartbeat_interval = event_data["d"]["heartbeat_interval"] / 1000
        await ws_client.identify()

    @staticmethod
    def heartbeat_hack(ws_client, event_data):
        ws_client.heartbeats.append(event_data)


# TODO: replace Dict with discord typing
WSEHandlerMapping = Dict[GatewayOpcode, Callable[[Dict], None]]


def setup_ws_event_handler(ws_client: WebsocketClient) -> WSEHandlerMapping:
    return {
        GatewayOpcode.DISPATCH: partial(WSEHandler.dispatch, ws_client),
        GatewayOpcode.HEARTBEAT: partial(WSEHandler.heartbeat, ws_client),
        GatewayOpcode.RECONNECT: partial(WSEHandler.reconnect, ws_client),
        GatewayOpcode.INVALID_SESSION: partial(WSEHandler.invalid_session, ws_client),
        GatewayOpcode.HELLO: partial(WSEHandler.hello, ws_client),
        GatewayOpcode.HEARTBEAT_ACK: partial(WSEHandler.heartbeat_hack, ws_client),
    }
