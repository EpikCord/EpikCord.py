from typing import Dict, List, Optional

from ..application import (
    Application,
    ApplicationCommand,
    ApplicationCommandPermission,
    GuildApplicationCommandPermission,
)
from ..exceptions import (
    InvalidApplicationCommandOptionType,
    InvalidApplicationCommandType,
)
from ..flags import Permissions
from ..options import *


class ClientApplication(Application):
    def __init__(self, client, data: dict):
        super().__init__(data)
        self.client = client

    async def fetch(self):
        response = await self.client.http.get("oauth2/applications/@me")
        data: dict = await response.json()
        return Application(data)

    async def fetch_global_application_commands(
        self, *, with_localizations: bool = False, with_localisations: bool = False
    ) -> List[ApplicationCommand]:
        with_localisation = with_localisations or with_localizations
        response = await self.client.http.get(
            f"/applications/{self.id}/commands?with_localizations={with_localisation}"
        )
        payload = [ApplicationCommand(command) for command in await response.json()]
        self.client.application_commands = payload
        return payload

    async def create_global_application_command(
        self,
        *,
        name: str,
        description: str,
        options: Optional[List[AnyOption]],
        default_member_permission: Optional[Permissions] = None,
        command_type: Optional[int] = 1,
        dm_permission: bool = True,
    ):
        payload = {
            "name": name,
            "description": description,
            "default_permissions": default_member_permission,
            "dm_permissions": dm_permission,
        }

        if command_type not in range(1, 4):
            raise InvalidApplicationCommandType("Command type must be 1, 2, or 3.")

        payload["type"] = command_type

        for option in options:
            if not isinstance(
                option,
                (
                    Subcommand,
                    SubCommandGroup,
                    StringOption,
                    IntegerOption,
                    BooleanOption,
                    UserOption,
                    ChannelOption,
                    RoleOption,
                    MentionableOption,
                    NumberOption,
                    AttachmentOption,
                ),
            ):
                raise InvalidApplicationCommandOptionType(
                    f"Options must be of type Subcommand, SubCommandGroup, "
                    f"StringOption, IntegerOption, BooleanOption, UserOption, "
                    f"ChannelOption, RoleOption, MentionableOption, "
                    f"NumberOption, not {option.__class__}. "
                )

        response = await self.client.http.post(
            f"/applications/{self.id}/commands", json=payload
        )
        return ApplicationCommand(await response.json())

    async def fetch_application_command(self, command_id: str):
        response = await self.client.http.get(
            f"/applications/{self.id}/commands/{command_id}"
        )
        return ApplicationCommand(await response.json())

    async def edit_global_application_command(
        self,
        command_id: str,
        *,
        name: Optional[str] = None,
        description: Optional[str] = None,
        options: Optional[List[AnyOption]] = None,
        default_permissions: Optional[bool] = None,
    ):
        payload = {}
        if name:
            payload["name"] = name
        if description:
            payload["description"] = description
        if options:
            payload["options"] = [option.to_dict() for option in options]
        if default_permissions:
            payload["default_permissions"] = default_permissions

        await self.client.http.patch(
            f"/applications/{self.id}/commands/{command_id}", json=payload
        )

    async def delete_global_app_command(self, command_id: str):
        await self.client.http.delete(f"/applications/{self.id}/commands/{command_id}")

    async def bulk_overwrite_global_app_commands(self, commands: List[Dict]):
        await self.client.http.put(f"/applications/{self.id}/commands", json=commands)

    async def fetch_guild_app_commands(self, guild_id: str):
        response = await self.client.http.get(
            f"/applications/{self.id}/guilds/{guild_id}/commands"
        )
        return [ApplicationCommand(command) for command in await response.json()]

    async def create_guild_app_command(
        self,
        guild_id: str,
        *,
        name: str,
        description: str,
        options=None,
        default_permission: Optional[bool] = False,
        command_type: Optional[int] = 1,
    ):
        if options is None:
            options = []

        payload = {
            "name": name,
            "description": description,
            "default_permissions": default_permission,
        }

        if command_type not in range(1, 4):
            raise InvalidApplicationCommandType("Command type must be 1, 2, or 3.")

        payload["type"] = command_type

        for option in options:
            if not isinstance(
                option,
                (
                    Subcommand,
                    SubCommandGroup,
                    StringOption,
                    IntegerOption,
                    BooleanOption,
                    UserOption,
                    ChannelOption,
                    RoleOption,
                    MentionableOption,
                    NumberOption.AttachmentOption,
                ),
            ):
                raise InvalidApplicationCommandOptionType(
                    f"Options must be of type Subcommand, SubCommandGroup, "
                    f"StringOption, IntegerOption, BooleanOption, UserOption, "
                    f"ChannelOption, RoleOption, MentionableOption, "
                    f"NumberOption, not {option.__class__}. "
                )

        response = await self.client.http.post(
            f"/applications/{self.id}/guilds/{guild_id}/commands", json=payload
        )
        return ApplicationCommand(await response.json())

    async def fetch_guild_application_command(self, guild_id: str, command_id: str):
        response = await self.client.http.get(
            f"/applications/{self.id}/guilds/{guild_id}/commands/{command_id}"
        )
        return ApplicationCommand(await response.json())

    async def edit_guild_application_command(
        self,
        guild_id: str,
        command_id: str,
        *,
        name: Optional[str] = None,
        description: Optional[str] = None,
        options: Optional[List[AnyOption]] = None,
        default_permissions: Optional[bool] = None,
    ):
        payload = {}
        if name:
            payload["name"] = name
        if description:
            payload["description"] = description
        if options:
            payload["options"] = [option.to_dict() for option in options]
        if default_permissions:
            payload["default_permissions"] = default_permissions

        await self.client.http.patch(
            f"/applications/{self.id}/guilds/{guild_id}/commands/{command_id}",
            json=payload,
        )

    async def delete_guild_application_command(self, guild_id: str, command_id: str):
        await self.client.http.delete(
            f"/applications/{self.id}/guilds/{guild_id}/commands/{command_id}"
        )

    async def bulk_overwrite_guild_application_commands(
        self, guild_id: str, commands: List[Dict]
    ):
        await self.client.http.put(
            f"/applications/{self.id}/guilds/{guild_id}/commands", json=commands
        )

    async def fetch_guild_application_command_permissions(
        self, guild_id: str, command_id: str
    ):
        response = await self.client.http.get(
            f"/applications/{self.id}/guilds/{guild_id}/commands/{command_id}/permissions"
        )
        return [
            GuildApplicationCommandPermission(command)
            for command in await response.json()
        ]

    async def edit_application_command_permissions(
        self,
        guild_id: str,
        command_id,
        *,
        permissions: List[ApplicationCommandPermission],
    ):
        payload = [permission.to_dict() for permission in permissions]
        await self.client.http.put(
            f"/applications/{self.id}/guilds/{guild_id}/commands/{command_id}/permissions",
            json=payload,
        )


__all__ = ("ClientApplication",)
