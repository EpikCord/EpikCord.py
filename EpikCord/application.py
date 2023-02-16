from discord_typings import ApplicationData
from discord_typings import InstallParams as InstallParamsData
from discord_typings import TeamData, TeamMemberData

from .flags import ApplicationFlags, Permissions
from .utils import TeamMembershipState, instance_or_none, int_or_none


class InstallParams:
    def __init__(self, data: InstallParamsData):
        self.scopes = data["scopes"]
        self.permissions = Permissions(int(data["permissions"]))


class TeamMember:
    def __init__(self, data: TeamMemberData):
        self.membership_state = TeamMembershipState(data["membership_state"])
        self.permissions = data["permissions"]
        self.team_id = int(data["team_id"])
        self.user = data["user"]  # TODO: User Object


class Team:
    def __init__(self, data: TeamData):
        self.icon = data["icon"]
        self.id = int(data["id"])
        self.members = [TeamMember(member) for member in data["members"]]
        self.name = data["name"]
        self.owner_user_id = int(data["owner_user_id"])


class Application:
    def __init__(self, data: ApplicationData):
        self.id = int(data["id"])
        self.name = data["name"]
        self.icon = data.get("icon")
        self.description = data["description"]
        self.rpc_origins = data.get("rpc_origins")
        self.bot_public = data["bot_public"]
        self.bot_require_code_grant = data["bot_require_code_grant"]
        self.terms_of_service_url = data.get("terms_of_service_url")
        self.privacy_policy_url = data.get("privacy_policy_url")
        self.owner = data.get("owner")  # TODO: User Object
        self.verify_key = data["verify_key"]
        self.team = instance_or_none(Team, data.get("team"))
        self.guild_id = int_or_none(data.get("guild_id"))
        self.primary_sku_id = int_or_none(data.get("primary_sku_id"))
        self.slug = data.get("slug")
        self.cover_image = data.get("cover_image")
        self.flags = instance_or_none(ApplicationFlags, data.get("flags"))
        self.tags = data.get("tags")
        self.install_params = instance_or_none(
            InstallParams, data.get("install_params")
        )
        self.custom_install_url = data.get("custom_install_url")
        self.role_connections_verification_url = data.get(
            "role_connections_verification_url"
        )
