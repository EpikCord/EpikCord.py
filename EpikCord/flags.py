from __future__ import annotations

from typing import Any, Dict, List


class Flag:
    class_flags: Dict[str, int]

    def __init_subclass__(cls) -> None:
        cls.class_flags = {
            k: v for k, v in cls.__dict__.items() if isinstance(v, int)
        }

    def __init__(self, value: int = 0, **kwargs):
        self.value = value
        self.turned_on: List[str] = [k for k, a in kwargs.items() if a]

        for k, v in self.class_flags.items():
            if v & value and k not in self.turned_on:
                self.turned_on.append(k)

        self.calculate_from_turned()

    def calculate_from_turned(self):
        value = 0
        for key, flag in self.class_flags.items():
            if key in self.class_flags:
                value |= flag
        self.value = value

    def __getattribute__(self, __name: str) -> Any:
        original = super().__getattribute__
        if __name in original("class_flags"):
            return __name in original("turned_on")
        return original(__name)

    def __setattr__(self, __name: str, __value: Any) -> None:
        if __name not in self.class_flags:
            return super().__setattr__(__name, __value)
        if __value and __name not in self.turned_on:
            self.turned_on.append(__name)
        elif not __value and __name in self.turned_on:
            self.turned_on.remove(__name)
        self.calculate_from_turned()

    @classmethod
    def all(cls):
        return cls(**{k: True for k in cls.class_flags})


class Intents(Flag):
    GUILDS = 1 << 0
    GUILD_MEMBERS = 1 << 1
    GUILD_MODERATION = 1 << 2
    GUILD_EMOJIS_AND_STICKERS = 1 << 3
    GUILD_INTEGRATIONS = 1 << 4
    GUILD_WEBHOOKS = 1 << 5
    GUILD_INVITES = 1 << 6
    GUILD_VOICE_STATES = 1 << 7
    GUILD_PRESENCES = 1 << 8
    GUILD_MESSAGES = 1 << 9
    GUILD_MESSAGE_REACTIONS = 1 << 10
    GUILD_MESSAGE_TYPING = 1 << 11
    DIRECT_MESSAGES = 1 << 12
    DIRECT_MESSAGE_REACTIONS = 1 << 13
    DIRECT_MESSAGE_TYPING = 1 << 14
    MESSAGE_CONTENT = 1 << 15
    GUILD_SCHEDULED_EVENTS = 1 << 16
    AUTO_MODERATION_CONFIGURATION = 1 << 20
    AUTO_MODERATION_EXECUTION = 1 << 21


class SystemChannelFlags(Flag):
    SUPPRESS_JOIN_NOTIFICATIONS = 1 << 0
    SUPPRESS_PREMIUM_SUBSCRIPTIONS = 1 << 1
    SUPPRESS_GUILD_REMINDER_NOTIFICATIONS = 1 << 2
    SUPPRESS_JOIN_NOTIFICATION_REPLIES = 1 << 3
    SUPPRESS_ROLE_SUBSCRIPTION_PURCHASE_NOTIFICATIONS = 1 << 4
    SUPPRESS_ROLE_SUBSCRIPTION_PURCHASE_NOTIFICATION_REPLIES = 1 << 5


class Permissions(Flag):
    CREATE_INSTANT_INVITE = 1 << 0
    KICK_MEMBERS = 1 << 1
    BAN_MEMBERS = 1 << 2
    ADMINISTRATOR = 1 << 3
    MANAGE_CHANNELS = 1 << 4
    MANAGE_GUILD = 1 << 5
    ADD_REACTIONS = 1 << 6
    VIEW_AUDIT_LOG = 1 << 7
    PRIORITY_SPEAKER = 1 << 8
    STREAM = 1 << 9
    READ_MESSAGES = 1 << 10
    SEND_MESSAGES = 1 << 11
    SEND_TTS_MESSAGES = 1 << 12
    MANAGE_MESSAGES = 1 << 13
    EMBED_LINKS = 1 << 14
    ATTACH_FILES = 1 << 15
    MENTION_EVERYONE = 1 << 17
    USE_EXTERNAL_EMOJIS = 1 << 18
    CONNECT = 1 << 20
    SPEAK = 1 << 21
    MUTE_MEMBERS = 1 << 22
    DEAFEN_MEMBERS = 1 << 23
    MOVE_MEMBERS = 1 << 24
    USE_VOICE_ACTIVATION = 1 << 25
    CHANGE_NICKNAME = 1 << 26
    MANAGE_NICKNAMES = 1 << 27
    MANAGE_ROLES = 1 << 28
    MANAGE_WEBHOOKS = 1 << 29
    MANAGE_EMOJIS_AND_STICKERS = 1 << 30
    USE_APPLICATION_COMMANDS = 1 << 31
    REQUEST_TO_SPEAK = 1 << 32
    MANAGE_EVENTS = 1 << 33
    MANAGE_THREADS = 1 << 34
    CREATE_PUBLIC_THREADS = 1 << 35
    CREATE_PRIVATE_THREADS = 1 << 36
    USE_EXTERNAL_STICKERS = 1 << 37
    SEND_MESSAGES_IN_THREADS = 1 << 38
    START_EMBEDDED_ACTIVITIES = 1 << 39
    MODERATOR_MEMBERS = 1 << 40


class ChannelFlags(Flag):
    PINNED = 1 << 1
    REQUIRE_TAG = 1 << 4
