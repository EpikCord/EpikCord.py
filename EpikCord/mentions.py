from .user import User
from .member import GuildMember

class MentionedChannel:
    def __init__(self, data: dict):
        self.id: str = data["id"]
        self.guild_id: str = data["guild_id"]
        self.type: int = data["type"]
        self.name: str = data["name"]
        
class MentionedUser(User):
    def __init__(self, client, data: dict):
        super().__init__(client, data)
        self.member = GuildMember(data["member"])