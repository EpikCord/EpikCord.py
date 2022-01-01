class PartialUser:
    def __init__(self, data: dict):
        self.data: dict = data
        self.avatar: str = data["avatar"]
        self.discriminator: str = data["discriminator"]
        self.id: str = data["id"]
        self.username: str = data["username"]