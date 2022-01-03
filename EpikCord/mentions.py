class MentionedChannel:
    def __init__(self, data: dict):
        self.id: str = data["id"]
        self.guild_id: str = data["guild_id"]
        self.type: int = data["type"]
        self.name: str = data["name"]
        
