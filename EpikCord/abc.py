from .exceptions import (
    InvalidArgumentType,
    CustomIdIsTooBig
)
    
class BaseChannel:
    def __init__(self, client, data: dict):
        self.id: str = data["id"]
        self.client = client
        self.type = data["type"]

class BaseComponent:
    def __init__(self):
        self.settings = {}

    def set_custom_id(self, custom_id: str):
        
        if not isinstance(custom_id, str):
            raise InvalidArgumentType("Custom Id must be a string.")
        
        elif len(custom_id) > 100:
            raise CustomIdIsTooBig("Custom Id must be 100 characters or less.")

        self.settings["custom_id"] = custom_id