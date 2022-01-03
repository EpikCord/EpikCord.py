from .user import User

class MessageInteraction: # https://discord.com/developers/docs/interactions/receiving-and-responding#message-interaction-object-message-interaction-structure idk
    def __init__(self, data: dict):
        self.id: str = data["id"]
        self.user: User = User(data["user"])
        self.name: str = data["name"]
        self.type: int = data["type"]