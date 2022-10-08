from __future__ import annotations

import asyncio
from sys import platform
from typing import TYPE_CHECKING, List, Optional

from .client import HTTPClient, WebsocketClient
from .flags import Intents
from .opcodes import GatewayOpcode
from .presence import Presence
from .utils import Utils

if TYPE_CHECKING:
    import discord_typings


class Shard(WebsocketClient):
    def __init__(
        self,
        token: str,
        intents: Intents,
        shard_id,
        number_of_shards,
        presence: Optional[Presence] = None,
        discord_endpoint: str = "https://discord.com/api/v10",
    ):
        super().__init__(token, intents, presence, discord_endpoint)
        self.shard_id = [shard_id, number_of_shards]

    async def ready(self, data: dict):
        self.session_id: str = data["session_id"]

    async def identify(self):
        payload = {
            "op": GatewayOpcode.IDENTIFY,
            "d": {
                "token": self.token,
                "intents": self.intents.value,
                "properties": {
                    "os": platform,
                    "browser": "EpikCord.py",
                    "device": "EpikCord.py",
                },
                "shard": str(self.shard_id),
            },
        }

        if self.presence:
            payload["d"]["presence"] = self.presence.to_dict()

        await self.send_json(payload)

    async def reconnect(self):
        await self.close()
        await self.connect()
        await self.identify()
        await self.resume()


class ShardManager:
    def __init__(
        self,
        token: str,
        intents: Intents,
        *,
        shards: Optional[int] = None,
        overwrite_commands_on_ready: bool = False,
        discord_endpoint: Optional[str] = None,
        presence: Optional[Presence] = None,
    ):
        super().__init__()
        self.token: str = token
        self.overwrite_commands_on_ready: bool = overwrite_commands_on_ready
        from EpikCord import __version__

        self.http: HTTPClient = HTTPClient(
            token,
            headers={
                "Authorization": f"Bot {token}",
                "User-Agent": f"DiscordBot (https://github.com/EpikCord/EpikCord.py {__version__})",
            },
        )
        self.intents: Intents = (
            intents if isinstance(intents, Intents) else Intents(intents)  # type: ignore
        )
        self.desired_shards: Optional[int] = shards
        self.shards: List[Shard] = []
        self.presence: Optional[Presence] = presence
        self.discord_endpoint: Optional[str] = discord_endpoint

    def run(self):
        async def wrapper():
            endpoint_data = await self.http.get("/gateway/bot")  # ClientResponse
            endpoint_data = await endpoint_data.json()  # Dict

            max_concurrency = endpoint_data["session_start_limit"]["max_concurrency"]

            shards = self.desired_shards or endpoint_data["shards"]

            for shard_id in range(shards):
                self.shards.append(
                    Shard(
                        self.token,
                        self.intents,
                        shard_id,
                        shards,
                        self.presence,
                        self.discord_endpoint,
                    )
                )

            current_iteration = 0  # The current shard_id we've run

            for shard in self.shards:
                shard.events = self.events
                await shard.login()
                await shard.wait_for("ready")

                current_iteration += 1

                if current_iteration == max_concurrency:
                    await asyncio.sleep(5)
                    current_iteration = 0  # Reset it

            if self.overwrite_commands_on_ready:
                for shard in self.shards:
                    await Utils(shard).override_commands()

        loop = asyncio.get_event_loop()
        loop.run_until_complete(wrapper())


__all__ = ("Shard", "ShardManager")
