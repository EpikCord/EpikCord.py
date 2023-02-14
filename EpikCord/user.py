from typing import Optional

from .utils import Locale, PremiumType
from .flags import UserFlags

from discord_typings import UserData


class User:
    def __init__(self, data: UserData):
        self.id: int = int(data["id"])
        self.username: str = data["username"]
        self.discriminator: str = data["discriminator"]
        self.avatar: Optional[str] = data.get("avatar")
        self.bot: Optional[bool] = data.get("bot")
        self.system: Optional[bool] = data.get("system")
        self.mfa_enabled: Optional[bool] = data.get("mfa_enabled")
        self.banner: Optional[str] = data.get("banner")
        self.accent_color: Optional[int] = int(data["accent_color"]) if "accent_color" in data and data["accent_color"] else None
        self.locale: Optional[Locale] = Locale(data["locale"]) if "locale" in data else None
        self.verified: Optional[bool] = data.get("verified")
        self.email: Optional[str] = data.get("email")
        self.flags: Optional[UserFlags] = UserFlags(data["flags"]) if "flags" in data else None
        self.premium_type: Optional[PremiumType] = PremiumType(data["premium_type"]) if "premium_type" in data else None
        self.public_flags: Optional[UserFlags] = UserFlags(data["public_flags"]) if "public_flags" in data else None