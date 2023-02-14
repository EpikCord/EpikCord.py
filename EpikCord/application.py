from typing import List, Optional
from .utils import TeamMemberMembershipState
from .flags import Permissions, ApplicationFlags
from discord_typings import ApplicationData, InstallParams as InstallParamsData, TeamData, TeamMemberData

class InstallParams:
    def __init__(self, data: InstallParamsData):
        self.scopes: List[str] = data["scopes"]
        self.permissions: Permissions = Permissions(int(data["permissions"]))

class TeamMember:
    def __init__(self, data: TeamMemberData):
        self.membership_state: TeamMemberMembershipState = TeamMemberMembershipState(data["membership_state"])
        self.permissions: List[str] = data["permissions"]
        self.team_id: int = int(data["team_id"])
        self.user = data["user"] # TODO: User Object

class Team:
    def __init__(self, data: TeamData):
        self.icon: Optional[str] = data["icon"]
        self.id: int = int(data["id"])
        self.members: List[TeamMember] = [TeamMember(member) for member in data["members"]]
        self.name: str = data["name"]
        self.owner_user_id: int = int(data["owner_user_id"])

class Application:
    def __init__(self, data: ApplicationData):
        self.id: int = int(data["id"])
        self.name: str = data["name"]
        self.icon: Optional[str] = data.get("icon")
        self.description: str = data["description"]
        self.rpc_origins: Optional[List[str]] = data.get("rpc_origins")
        self.bot_public: bool = data["bot_public"]
        self.bot_require_code_grant: bool = data["bot_require_code_grant"]
        self.terms_of_service_url: Optional[str] = data.get("terms_of_service_url")
        self.privacy_policy_url: Optional[str] = data.get("privacy_policy_url")
        self.owner = data.get("owner") # TODO: User Object
        self.verify_key: str = data["verify_key"]
        self.team: Optional[Team] = Team(data["team"]) if data["team"] else None
        self.guild_id: Optional[int] = int(data["guild_id"]) if "guild_id" in data else None
        self.primary_sku_id: Optional[int] = int(data["primary_sku_id"]) if "primary_sku_id" in data else None
        self.slug: Optional[str] = data["slug"] if "slug" in data else None
        self.cover_image: Optional[str] = data["cover_image"] if "cover_image" in data else None
        self.flags: Optional[ApplicationFlags] = ApplicationFlags(data["flags"]) if "flags" in data else None # TODO: Values
        self.tags: Optional[List[str]] = data["tags"] if "tags" in data else None
        self.install_params: Optional[InstallParams] = InstallParams(data["install_params"]) if "install_params" in data else None
        self.custom_install_url: Optional[str] = data["custom_install_url"] if "custom_install_url" in data else None
        self.role_connections_verification_url: Optional[str] = data["role_connections_verification_url"] if "role_connections_verification_url" in data else None
