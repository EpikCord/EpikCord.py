from typing import (
    Optional
)
from .partials import PartialUser

class User(PartialUser):
    def __init__(self, data: dict):
        super().__init__(data)
        self.bot: bool = data["bot"]
        self.system: bool = data["system"]
        self.mfa_enabled: bool = data["mfa_enabled"]
        self.banner: Optional[str] = data["banner"] or None
        self.accent_color: Optional[int] = data["accent_color"] or None # the user's banner color encoded as an integer representation of hexadecimal color code	
        self.locale: Optional[str] = data["locale"] or None
        self.verified: bool = data["verified"]
        self.email: Optional[str] = data["email"] or None
        self.flags: int = data["flags"]
        self.premium_type: int = data["premium_type"]
        self.public_flags: int = data["public_flags"]