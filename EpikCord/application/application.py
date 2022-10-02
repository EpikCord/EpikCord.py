from typing import TYPE_CHECKING, List, Optional

from ..partials import PartialUser
from .team import Team

if TYPE_CHECKING:
    import discord_typings


def _filter_values(dictionary: dict) -> dict:
    return {k: v for k, v in dictionary.items() if v is not None}


class Application:
    def __init__(self, data: discord_typings.ApplicationData):
        self.id: int = int(data["id"])
        self.name: str = data["name"]
        self.icon: Optional[str] = data.get("icon")
        self.description: str = data["description"]
        self.rpc_origins: Optional[List[str]] = data.get("rpc_origins")
        self.bot_public: bool = data["bot_public"]
        self.bot_require_code_grant: bool = data["bot_require_code_grant"]
        self.terms_of_service_url: Optional[str] = data.get("terms_of_service")
        self.privacy_policy_url: Optional[str] = data.get("privacy_policy")
        self.owner: Optional[PartialUser] = (
            PartialUser(data["owner"]) if "user" in data else None
        )
        self.verify_key: str = data["verify_key"]
        self.team: Optional[Team] = Team(data["team"]) if data["team"] else None
        self.cover_image: Optional[str] = data.get("cover_image")
        self.flags: Optional[int] = data.get("flags")

    def to_dict(self):
        return _filter_values(
            {
                "id": self.id,
                "name": self.name,
                "description": self.description,
                "rpc_origins": self.rpc_origins,
                "bot_public": self.bot_public,
                "bot_require_code_grant": self.bot_require_code_grant,
                "terms_of_service_url": self.terms_of_service_url,
                "privacy_policy_url": self.privacy_policy_url,
                "verify_key": self.verify_key.to_dict(),
                "team": self.team.to_dict() if self.team else None,
                "cover_image": self.cover_image,
                "flags": self.flags,
            }
        )  # A dict of things that aren't private and return a Truthy value.


__all__ = ("Application",)
