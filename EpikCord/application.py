from .team import Team
from .partials import PartialUser
from typing import (
    Optional
)

class Application:
    def __init__(self, data: dict):
        self.id: str = data["id"]
        self.name: str = data["name"]
        self.icon: Optional[str] = data["icon"] or None
        self.description: str = data["description"]
        self.rpc_origins: Optional[list] = data["rpc_origins"] or None
        self.bot_public: bool = data["bot_public"]
        self.bot_require_code_grant: bool = data["bot_require_code_grant"]
        self.terms_of_service_url: Optional[str] = data["terms_of_service"] or None
        self.privacy_policy_url: Optional[str] = data["privacy_policy"] or None
        self.owner: PartialUser = PartialUser(data["user"])
        self.summary: str = data["summary"]
        self.verify_key: str = data["verify_key"]
        self.team: Optional[Team] = Team(data["team"])
        self.flags: int = data["flags"]
