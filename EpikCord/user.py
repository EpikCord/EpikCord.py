from discord_typings import UserData

from .client import Client
from .flags import UserFlags
from .utils import Locale, PremiumType, instance_or_none, int_or_none


class User:
    def __init__(self, client: Client, data: UserData):
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
