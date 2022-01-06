class Overwrite:
    def __init__(self, data: dict):
        self.id: str = data["id"]
        self.type: int = data["type"]
        self.allow: str = data["allow"]
        self.deny: str = data["deny"]