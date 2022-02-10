# Inspired by Discord.JS

class InteractionOptionsResolver:
    def __init__(self, option_data: dict):
        self.data: dict = option_data # In case we miss anything and people can just do it themselves
        self.users: dict = self.data["users"]
        self.users: dict = self.data["members"]
        self.roles: dict = self.data["roles"]
        self.channels: dict = self.data["channels"]
