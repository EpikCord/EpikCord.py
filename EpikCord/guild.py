from datetime import datetime

from discord_typings import GuildMemberData, RoleData, RoleTagsData

from .client import Client
from .flags import GuildMemberFlags, Permissions
from .user import User
from .utils import instance_or_none, int_or_none


class GuildMember:
    """
    Attributes:
    ----------
    client: :class:`Epikcord.py.client.Client`.
        ...
    user: :class:``
        The user itself.
    nick: :class:`str`
        The nickname the user uses in the guild.
    avatar: :class:`str`
        The avatar of the user in the guild.
    roles: :class:``
        The roles the user has.
    joined_at: :class:`datetime.datetime.fromisoformat`
        When the client joined the guild.
    premium_since: :class:`datetime.datetime.fromisoformat`
        How long the member has premium.
    deaf: :class:``
        If the member is deafend.
    mute: :class:``
        If the member is muted.
    flags: :class:``
        The flags the member has.
    pending: :class:``
        ...
    permissions: :class:``
        The permissions the member has.
    communication_disabled_until: :class:``
        How long the member has communication disabled.
    """
    def __init__(self, client: Client, data: GuildMemberData):
        """
        Parameters:
        -----------
        client: :class:`Epikcord.py.client.Client`
            The bot itself.
        data: :class:`discord_typings.GuildMemberData
            The data about the member in the guild.
        """
        self.client = client
        self.user = instance_or_none(
            User, data.get("user"), client, data.get("user"), ignore_value=True
        )
        self.nick = data.get("nick")
        self.avatar = data.get("avatar")
        # self.roles = [Role(client, role) for role in data.get("roles", [])]
        self.roles = data["roles"]
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

        raw_flags = data["flags"]  # type: ignore # DiscordTyping/32
        self.flags = GuildMemberFlags(raw_flags)
        self.pending = data.get("pending")
        self.permissions = instance_or_none(
            Permissions, data.get("permissions")
        )
        self.communication_disabled_until = instance_or_none(
            datetime.fromisoformat, data.get("communication_disabled_until")
        )


class RoleTags:
    """
    Attributes:
    ----------
    bot_id: :class:`int`
        ...
    integration_id: :class:`int`
        ...
    premium_subscriber: :class:`bool`
        ...
    available_for_purchase: :class:`bool`
        ...
    guild_connections: :class:`bool`
        ...
    """
    def __init__(self, data: RoleTagsData):
        """
        Parameters:
        ----------
        data: :class:`discord_typings.RoleTagsData`
            Data containing Role Tags.
        """
        self._data = data
        self.bot_id = int_or_none(data.get("bot_id"))
        self.integration_id = int_or_none(data.get("integration_id"))
        self.premium_subscriber = bool(data.get("premium_subscriber"))
        self.subscription_listing_id = int_or_none(
            data.get("subscription_listing_id")
        )
        self.available_for_purchase = bool(data.get("available_for_purchase"))
        self.guild_connections = bool(data.get("guild_connections"))


class Role:
    """
    Attributes:
    ----------
    client: :class:`Epikcord.py.client.Client`
        The bot itself.
    id: :class:`int`
        The id of the role.
    name: :class:`str`
        The name given to the role.
    color: :class:`int`
        The color given to the role.
    hoist: :class:``
        ...
    icon: :class:``
        The icon of the role.
    unicode_emoji: :class:``
        ...
    position: :class:``
        The position the role is in (in a hierarchy).
    permissions: :class:`Epikcord.py.flags.Permissions`
        The permission the role has.
    managed: :class:``
        ...
    mentionable: :class:``
        If the role is pingable
    tags: :class:`Epikcord.py.guild.RoleTags`
        ...
    """
    def __init__(self, client: Client, data: RoleData):
        """
        Parameters:
        -----------
        client: :class:`Epikcord.py.client.Client`
            The bot itself
        data: :class:`discord_typings.RoleData`
            Data containing about the role
        """
        self.client = client
        self._data = data
        self.id = int(data["id"])
        self.name = data["name"]
        self.color = int(data["color"])
        self.hoist = data["hoist"]
        self.icon = data.get("icon")
        self.unicode_emoji = data.get("unicode_emoji")
        self.position = data["position"]
        self.permissions = Permissions(int(data["permissions"]))
        self.managed = data["managed"]
        self.mentionable = data["mentionable"]
        self.tags = instance_or_none(RoleTags, data.get("tags"))
