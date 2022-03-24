from typing import Optional
from .exceptions import InvalidIntents
class Intents:
    def __init__(self, *, intents: Optional[int] = None):
        self.value = intents or 0

    @property
    def guilds(self):
        self.value += 1 << 0
        return self

    @property
    def guild_members(self):
        self.value += 1 << 1
        return self

    @property
    def guild_bans(self):
        self.value += 1 << 2
        return self

    @property
    def guild_emojis_and_stickers(self):
        self.value += 1 << 3
        return self

    @property
    def guild_integrations(self):
        self.value += 1 << 4
        return self

    @property
    def guild_webhooks(self):
        self.value += 1 << 5
        return self

    @property
    def guild_invites(self):
        self.value += 1 << 6
        return self

    @property
    def guild_voice_states(self):
        self.value += 1 << 7
        return self

    @property
    def guild_presences(self):
        self.value += 1 << 8
        return self

    @property
    def guild_messages(self):
        self.value += 1 << 9
        return self

    @property
    def guild_message_reactions(self):
        self.value += 1 << 10
        return self

    @property
    def guild_message_typing(self):
        self.value += 1 << 11
        return self

    @property
    def direct_messages(self):
        self.value += 1 << 12
        return self

    @property
    def direct_message_reactions(self):
        self.value += 1 << 13
        return self

    @property
    def direct_message_typing(self):
        self.value += 1 << 14
        return self

    @property
    def all(self):
        for attr in dir(self):
            if attr not in ["value", "all", "none", "remove_value", "add_intent"]:
                getattr(self, attr)
        return self

    @property
    def none(self):
        self.value = 0

    def remove_intent(self, intent: str) -> int:
        try:
            attr = getattr(self, intent.lower())
        except AttributeError:
            raise InvalidIntents(
                f"Intent {intent.lower()} is not a valid intent.")
        self.value -= attr.value
        return self.value

    def add_intent(self, intent: str) -> int:
        try:
            attr = getattr(self, intent)
        except AttributeError:
            raise InvalidIntents(f"Intent {intent} is not a valid intent.")
        self.value += attr
        return self.value

    @property
    def message_content(self):
        self.value += 1 << 15
        return self