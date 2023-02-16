from datetime import datetime

from discord_typings import GuildMemberData

from .client import Client
from .flags import GuildMemberFlags, Permissions
from .user import User
from .utils import instance_or_none


class GuildMember:
    def __init__(self, client: Client, data: GuildMemberData):
        self.client = client
        self.user = instance_or_none(
            User, data.get("user"), client, data.get("user"), ignore_value=True
        )
        self.nick = data.get("nick")
        self.avatar = data.get("avatar")
        self.roles = data.get("roles")  # TODO: Add Role Object
        self.joined_at = (
            datetime.fromisoformat(data["joined_at"])
            if data.get("joined_at")
            else None
        )
        self.premium_since = instance_or_none(
            datetime.fromisoformat, data.get("premium_since")
        )
        self.deaf = data["deaf"]
        self.mute = data["mute"]
        self.flags = GuildMemberFlags(data["flags"])  # type: ignore # DiscordTyping/32
        self.pending = data.get("pending")
        self.permissions = instance_or_none(
            Permissions, data.get("permissions")
        )
        self.communication_disabled_until = instance_or_none(
            datetime.fromisoformat, data.get("communication_disabled_until")
        )
