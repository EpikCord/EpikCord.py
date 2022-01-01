from .partials import PartialUser

from typing import (
    List,
    Optional
)

class TeamMember:
    def __init__(self, data: dict):
        self.data = data
        self.membership_state: int = data["membership_state"]
        self.team_id: str = data["team_id"]
        self.user: PartialUser = PartialUser(data["user"])

class Team:
    def __init__(self,data: dict):
        self.data = data
        self.icon: str = data["icon"]
        self.id: str = data["id"]
        self.members: List[TeamMember] = data["members"]