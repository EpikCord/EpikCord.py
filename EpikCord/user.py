from discord_typings import UserData

from .client import Client
from .flags import UserFlags
from .locales import Locale
from .utils import PremiumType, instance_or_none, int_or_none


class User:
    """
    Attributes:
    ----------
    client: :class:`Epikcord.client.Client`
        The bot itself
    id: :class:`int`
        The id of the user
    username: :class:`str`
        The name of the user
    discriminator: :class:`int`
        The 4 digit number on user's profile
    avatar: :class:``
        The avatar ...
    bot: :class:`bool`
        If the user is a bot
    system: :class:``
        ...
    mfa_enabled: :class:`bool`
        If the user enabled mfa (Multi factor authentication)
    banner: :class:``
        The banner on the user's profile
    accent_color: :class:``
        The accent color the user has on his profile
    locale: :class:`Epikcord.utils.Locale`
        ...
    verified: :class:`bool`
        If the user is verified
    email: :class:`str`
        The email of the user
    premium_type: :class:`Epikcord.utils.PremiumType`
        The type of premium the user has (Nitro Basic or Nitro)
    public_flags: :class:`Epikcord.flags.UserFlags`
        The public flags the user has
    """
    def __init__(self, client: Client, data: UserData):
        """
        Parameters:
        -----------
        client: :class:`Epikcord.client.Client`
            The bot itself
        data: :class:`discord_typings.UserData`
            Data containing about the user
        """
        self.client = client
        self.id = int(data["id"])
        self.username = data["username"]
        self.discriminator = data["discriminator"]
        self.avatar = data.get("avatar")
        self.bot = data.get("bot")
        self.system = data.get("system")
        self.mfa_enabled = data.get("mfa_enabled")
        self.banner = data.get("banner")
        self.accent_color = int_or_none(data.get("accent_color"))
        self.locale = instance_or_none(Locale, data.get("locale"))
        self.verified = data.get("verified")
        self.email = data.get("email")
        self.flags = instance_or_none(UserFlags, data.get("flags"))
        self.premium_type = instance_or_none(
            PremiumType, data.get("premium_type")
        )
        self.public_flags = instance_or_none(
            UserFlags, data.get("public_flags")
        )
        self._data: UserData = data
