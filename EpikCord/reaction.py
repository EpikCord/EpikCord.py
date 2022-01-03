from .partials import PartialEmoji

class Reaction:
    def __init__(self, data: dict):
        self.count: int = data["count"]
        self.me: bool = data["me"]
        self.emoji: PartialEmoji = PartialEmoji(data["emoji"])