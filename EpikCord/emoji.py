class PartialEmoji:
    def __init__(self, data: dict):
        self.data: dict = data
        self.name: str = data.get("name")
        self.id: str = data.get("id")
        self.animated: bool = data.get("animated")

    def to_dict(self):
        payload = {
            "id": self.id,
            "name": self.name,
        }

        if self.animated in (True, False):
            payload["animated"] = self.animated

        return payload