import datetime
from .errors import InvalidApplicationCommandType, InvalidApplicationCommandOptionType
from .member import User, PartialUser
from .slash import (
    AnyOption, 
    Subcommand, 
    SubCommandGroup, 
    StringOption, 
    BooleanOption, 
    IntegerOption, 
    UserOption, 
    ChannelOption, 
    RoleOption, 
    MentionableOption, 
    NumberOption
)
from typing import Optional, List

class Application:
    def __init__(self, data: dict):
        self.id: str = data.get("id")
        self.name: str = data.get("name")
        self.icon: Optional[str] = data.get("icon")
        self.description: str = data.get("description")
        self.rpc_origins: Optional[list] = data.get("rpc_origins")
        self.bot_public: bool = data.get("bot_public")
        self.bot_require_code_grant: bool = data.get("bot_require_code_grant")
        self.terms_of_service_url: Optional[str] = data.get("terms_of_service")
        self.privacy_policy_url: Optional[str] = data.get("privacy_policy")
        self.owner: Optional[PartialUser] = PartialUser(data.get("user")) if data.get("user") else None
        self.summary: str = data.get("summary")
        self.verify_key: str = data.get("verify_key")
        self.team: Optional[Team] = Team(data.get("team")) if data.get("get") else None
        self.cover_image: Optional[str] = data.get("cover_image")
        self.flags: int = data.get("flags")

class TeamMember:
    def __init__(self, data: dict):
        self.data = data
        self.membership_state: int = data.get("membership_state")
        self.team_id: str = data.get("team_id")
        self.user: PartialUser = PartialUser(data.get("user"))


class Team:
    def __init__(self, data: dict):
        self.data = data
        self.icon: str = data.get("icon")
        self.id: str = data.get("id")
        self.members: List[TeamMember] = data.get("members")

class ApplicationCommandPermission:
    def __init__(self, data: dict):
        self.id: str = data.get("id")
        self.type: int = data.get("type")
        self.permission: bool = data.get("permission")

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "permission": self.permission
        }


class GuildApplicationCommandPermission:
    def __init__(self, data: dict):
        self.id: str = data.get("id")
        self.application_id: str = data.get("application_id")
        self.guild_id: str = data.get("guild_id")
        self.permissions: ApplicationCommandPermission = ApplicationCommandPermission(data.get("permissions"))

    def to_dict(self):
        return {
            "id": self.id,
            "application_id": self.application_id,
            "guild_id": self.guild_id,
            "permissions": self.permissions.to_dict()
        }

class ApplicationCommand:
    def __init__(self, data: dict):
        self.id: str = data.get("id")
        self.type: int = data.get("type")
        self.application_id: str = data.get("application_id")
        self.guild_id: Optional[str] = data.get("guild_id")
        self.name: str = data.get("name")
        self.description: str = data.get("description")
        self.default_permissions: bool = data.get("default_permissions")
        self.version: str = data.get("version")

class IntegrationAccount:
    def __init__(self, data: dict):
        self.id: str = data.get("id")
        self.name: str = data.get("name")

class Integration:
    def __init__(self, data: dict):
        self.id: str = data.get("id")
        self.name: str = data.get("name")
        self.type: str = data.get("type")
        self.enabled: bool = data.get("enabled")
        self.syncing: Optional[bool] = data.get("syncing")
        self.role_id: Optional[str] = data.get("role_id")
        self.expire_behavior: str = "REMOVE_ROLE" if data.get("expire_behavior") == 1 else "REMOVE_ACCOUNT" if data.get("expire_behavior") == 2 else None
        self.expire_grace_period: Optional[int] = data.get("expire_grace_period")
        self.user: Optional[User] = User(data.get("user")) if data.get("user") else None
        self.account: IntegrationAccount = IntegrationAccount(data.get("account"))
        self.synced_at: datetime.datetime = datetime.datetime.fromioformat(data.get("synced_at"))
        self.subscriber_count: int = data.get("subscriber_count")
        self.revoked: bool = data.get("revoked")
        self.application: Optional[Application] = Application(data.get("application")) if data.get("application") else None

class ClientApplication(Application):
    def __init__(self, client, data: dict):
        super().__init__(data)
        self.client = client

    async def fetch_application(self):
        response = await self.client.http.get("oauth2/applications/@me")
        data: dict = await response.json()
        return Application(data)

    async def fetch_global_application_commands(self) -> List[ApplicationCommand]:
        response = await self.client.http.get(f"/applications/{self.id}/commands")
        payload = [ApplicationCommand(command) for command in await response.json()]
        self.client.application_commands = payload
        return payload
    
    async def create_global_application_command(self,*, name: str, description: str, options: Optional[List[AnyOption]], default_permission: Optional[bool] = False, command_type: Optional[int] = 1):
        payload = {
            "name": name,
            "description": description,
            "default_permissions": default_permission
        }

        if command_type not in range(1, 4):
            raise InvalidApplicationCommandType("Command type must be 1, 2, or 3.")

        payload["type"] = command_type

        for option in options:
            if not isinstance(option, (Subcommand, SubCommandGroup, StringOption, IntegerOption, BooleanOption, UserOption, ChannelOption, RoleOption, MentionableOption, NumberOption. AttachmentOption)):
                raise InvalidApplicationCommandOptionType(f"Options must be of type Subcommand, SubCommandGroup, StringOption, IntegerOption, BooleanOption, UserOption, ChannelOption, RoleOption, MentionableOption, NumberOption, not {option.__class__}.")

        response = await self.client.http.post(f"/applications/{self.id}/commands", json = payload)
        return ApplicationCommand(await response.json())

    async def fetch_application_command(self, command_id: str):
        response = await self.client.http.get(f"/applications/{self.id}/commands/{command_id}")
        return ApplicationCommand(await response.json())

    async def edit_global_application_command(self, command_id: str, *, name: Optional[str] = None, description: Optional[str] = None, options: Optional[List[AnyOption]] = None, default_permissions: Optional[bool] = None):
        payload = {}
        if name:
            payload["name"] = name
        if description:
            payload["description"] = description
        if options:
            payload["options"] = [option.to_dict() for option in options]
        if default_permissions:
            payload["default_permissions"] = default_permissions
        
        await self.client.http.patch(f"/applications/{self.id}/commands/{command_id}", json=payload)

    async def delete_global_application_command(self, command_id: str):
        await self.client.http.delete(f"/applications/{self.id}/commands/{command_id}")

    async def bulk_overwrite_global_application_commands(self, commands: List[ApplicationCommand]):
        payload = [command for command in commands]
        await self.client.http.put(f"/applications/{self.id}/commands", json =  payload)

    async def fetch_guild_application_commands(self, guild_id: str):
        response = await self.client.http.get(f"/applications/{self.id}/guilds/{guild_id}/commands")
        return [ApplicationCommand(command) for command in await response.json()]

    async def create_guild_application_command(self, guild_id: str, *, name: str, description: str, options: Optional[List[AnyOption]] = [], default_permission: Optional[bool] = False, command_type: Optional[int] = 1):
        payload = {
            "name": name,
            "description": description,
            "default_permissions": default_permission
        }

        if command_type not in range(1, 4):
            raise InvalidApplicationCommandType("Command type must be 1, 2, or 3.")

        payload["type"] = command_type

        for option in options:
            if not isinstance(option, (Subcommand, SubCommandGroup, StringOption, IntegerOption, BooleanOption, UserOption, ChannelOption, RoleOption, MentionableOption, NumberOption. AttachmentOption)):
                raise InvalidApplicationCommandOptionType(f"Options must be of type Subcommand, SubCommandGroup, StringOption, IntegerOption, BooleanOption, UserOption, ChannelOption, RoleOption, MentionableOption, NumberOption, not {option.__class__}.")

        response = await self.client.http.post(f"/applications/{self.id}/guilds/{guild_id}/commands", json = payload)
        return ApplicationCommand(await response.json())

    async def fetch_guild_application_command(self, guild_id: str, command_id: str):
        response = await self.client.http.get(f"/applications/{self.id}/guilds/{guild_id}/commands/{command_id}")
        return ApplicationCommand(await response.json())

    async def edit_global_application_command(self, guild_id: str, command_id: str, *, name: Optional[str] = None, description: Optional[str] = None, options: Optional[List[AnyOption]] = None, default_permissions: Optional[bool] = None):
        payload = {}
        if name:
            payload["name"] = name
        if description:
            payload["description"] = description
        if options:
            payload["options"] = [option.to_dict() for option in options]
        if default_permissions:
            payload["default_permissions"] = default_permissions
        
        await self.client.http.patch(f"/applications/{self.id}/guilds/{guild_id}/commands/{command_id}", json = payload)

    async def delete_guild_application_command(self, guild_id: str, command_id: str):
        await self.client.http.delete(f"/applications/{self.id}/guilds/{guild_id}/commands/{command_id}")

    async def bulk_overwrite_guild_application_commands(self, guild_id: str, commands: List[ApplicationCommand]):
        payload = [command for command in commands]
        await self.client.http.put(f"/applications/{self.id}/guilds/{guild_id}/commands", json =  payload)

    async def fetch_guild_application_command_permissions(self, guild_id: str, command_id: str):
        response = await self.client.http.get(f"/applications/{self.id}/guilds/{guild_id}/commands/{command_id}/permissions")
        return [GuildApplicationCommandPermission(command) for command in await response.json()]

    async def edit_application_command_permissions(self, guild_id: str, command_id, *, permissions: List[ApplicationCommandPermission]):
        payload = [permission.to_dict() for permission in permissions]
        await self.client.http.put(f"/applications/{self.id}/guilds/{guild_id}/commands/{command_id}/permissions", json = payload)
