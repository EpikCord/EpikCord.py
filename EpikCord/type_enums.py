from enum import IntEnum, Enum


class VisibilityType(IntEnum):
    NONE = 0
    EVERYONE = 1


class ApplicationCommandPermissionType(IntEnum):
    ROLE = 1
    USER = 2
    CHANNEL = 3


class Locale(Enum):
    DANISH = "da"
    GERMAN = "de"
    ENGLISH_GB = "en-GB"
    ENGLISH_US = "en-US"
    SPANISH = "es-ES"
    FRENCH = "fr"
    CROATIAN = "hr"
    ITALIAN = "it"
    LITHUANIAN = "lt"
    HUNGARIAN = "hu"
    DUTCH = "nl"
    NORWEGIAN = "no"
    POLISH = "pl"
    PORTUGUESE_BR = "pt-BR"
    ROMANIAN = "ro"
    FINNISH = "fi"
    SWEDISH_SE = "sv-SE"
    VIETNAMESE = "vi"
    TURKISH = "tr"
    CZECH = "cs"
    GREEK = "el"
    BULGARIAN = "bg"
    RUSSIAN = "ru"
    UKRAINE = "uk"
    HINDI = "hi"
    THAI = "th"
    CHINESE_CN = "zh-CN"
    JAPANESE = "ja"
    CHINESE_TW = "zh-TW"
    KOREAN = "ko"


class AutoModActionType(IntEnum):
    BLOCK_MESSAGE = 1
    SEND_ALERT_MESSAGE = 2
    TIMEOUT = 3


class AutoModEventType(IntEnum):
    MESSAGE_SEND = 1


class AutoModTriggerType(IntEnum):
    KEYWORD = 1
    HARMFUL_LINK = 2
    SPAM = 3
    KEYWORD_PRESENT = 4


class AutoModKeywordPresetTypes(IntEnum):
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

__all__ = (
    "VisibilityType",
    "ApplicationCommandPermissionType",
    "Locale",
    "AutoModActionType",
    "AutoModEventType",
    "AutoModTriggerType",
    "AutoModKeywordPresetTypes",
    "ChannelTypes"
)