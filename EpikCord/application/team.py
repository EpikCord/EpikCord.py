from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional

from ..partials import PartialUser

if TYPE_CHECKING:
    import discord_typings


class TeamMember:
    def __init__(self, data: discord_typings.TeamMemberData):
        self.data = data
        self.membership_state: int = data["membership_state"]
        self.team_id: int = int(data["team_id"])
        self.user: PartialUser = PartialUser(data["user"])


class Team:
    def __init__(self, data: discord_typings.TeamData):
        self.data = data
        self.icon: Optional[str] = data.get("icon")
        self.id: int = int(data["id"])
        self.members: List[TeamMember] = [
            TeamMember(m) for m in data.get("members", [])
        ]


__all__ = ("Team", "TeamMember")
