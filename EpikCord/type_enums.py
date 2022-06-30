from enum import IntEnum

class AutoModerationActionType(IntEnum):
    BLOCK_MESSAGE = 1
    SEND_ALERT_MESSAGE = 2
    TIMEOUT = 3


class AutoModerationEventType(IntEnum):
    MESSAGE_SEND = 1


class AutoModerationTriggerType(IntEnum):
    KEYWORD = 1
    HARMFUL_LINK = 2
    SPAM = 3
    KEYWORD_PRESENT = 4


class AutoModerationKeywordPresetTypes(IntEnum):
    PROFANITY = 1
    SEXUAL_CONTENT = 2
    SLURS = 3


class ChannelTypes(IntEnum):
    GUILD_TEXT = 0
    DM = 1
    GUILD_VOICE = 2
    GUILD_CATEGORY = 4
    GUILD_NEWS = 5
    GUILD_NEWS_THREAD = 10
    GUILD_PUBLIC_THREAD = 11
    GUILD_PRIVATE_THREAD = 12
    GUILD_STAGE_VOICE = 13
    GUILD_DIRECTORY = 14
    GUILD_FORUM = 15