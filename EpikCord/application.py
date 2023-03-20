from discord_typings import ApplicationData
from discord_typings import InstallParams as InstallParamsData
from discord_typings import TeamData, TeamMemberData

from .flags import ApplicationFlags, Permissions
from .utils import TeamMembershipState, instance_or_none, int_or_none


class InstallParams:
    """
    Attributes:
    ----------
    scopes: :class:``
        ...
    permissions: :class:`Epikcord.py.flags.Permission`
        ...
    """
    def __init__(self, data: InstallParamsData):
        """
        Parameters:
        ----------
        data: :class:`discord_typings.InstallParamsData`
            ...
        """
        self.scopes = data["scopes"]
        self.permissions = Permissions(int(data["permissions"]))


class TeamMember:
    """
    Attributes:
    ----------
    membership_state: :class:`discord_typings.TeamMembershipState`
        ...
    permissions: :class:``
        ...
    team_id: :class:`int`
        The id of the team
    user: :class:``
        The user of the team
    """
    def __init__(self, data: TeamMemberData):
        """
        Parameters:
        ----------
        data: :class:`discord_typings.TeamMemberData`
            The data of the TeamMember
        """
        self.membership_state = TeamMembershipState(data["membership_state"])
        self.permissions = data["permissions"]
        self.team_id = int(data["team_id"])
        self.user = data["user"]  # TODO: User Object
        self._data: TeamMemberData = data


class Team:
    """
    Attributes:
    ----------
    icon: :class:``
        The icon of the team.
    id: :class:`int`
        The id of the team.
    members: :class:`list`
        The members in the team.
    name: :class:`str`
        The name of the team.
    owner_user_id: :class:`int`
        The owner id of the team.
    """
    def __init__(self, data: TeamData):
        """
        Parameters:
        ----------
        data: :class:`discord_typings.TeamData`
            The data of the team
        """
        self.icon = data["icon"]
        self.id = int(data["id"])
        self.members = [TeamMember(member) for member in data["members"]]
        self.name = data["name"]
        self.owner_user_id = int(data["owner_user_id"])


class Application:
    """
    Attributes:
    ----------
    id: :class:`int`
        The id of the application.
    name: :class:`str`
        The name of the application.
    icon: :class:``
        The icon of the application.
    description: :class:`str`
        The description of the application.
    rpc_origins: :class:``
        ...
    bot_public: :class:``
        ...
    bot_require_code_grant: :class:``
        ...
    terms_of_service_url: :class:`str`
        The Terms of Service url.
    privacy_policy_url = :class:`str`
        The Privacy Policy url 
    owner: :class:``
        The owner of the application.
    verify_key: :class:``
        ....
    team: :class:`Epikcord.py.application.Team`
        The team the application is in.
    guild_id: :class:`int`
        The id of guild
    primary_sku_id: :class:`int`
        ...
    slug: :class:``
        ...
    cover_image: :class:``
        ...
    flags: :class:`Epikcord.py.flags.ApplicationFlags`
        ...
    tags: :class:``
        ...
    install_params: :class:``
        ...
    self.custom_install_url: :class:``
        ...
    self.role_connections_verification_url: :class:``
        ...
    """
    def __init__(self, data: ApplicationData):
        """
        Paramters:
        ---------
        data: :class:`discord_typings.ApplicationData`
            The data of the Application
        """
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
        self._data: ApplicationData = data
