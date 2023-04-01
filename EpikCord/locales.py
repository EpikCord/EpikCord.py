from enum import Enum
from typing import Dict


class Locale(Enum):
    INDONESIAN = "id"
    DANISH = "da"
    GERMAN = "de"
    ENGLISH_UK = "en-GB"
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
    PORTUGUESE_BRAZILIAN = "pt-BR"
    ROMANIAN_ROMANIA = "ro"
    FINNISH = "fi"
    SWEDISH = "sv-SE"
    VIETNAMESE = "vi"
    TURKISH = "tr"
    CZECH = "cs"
    GREEK = "el"
    BULGARIAN = "bg"
    RUSSIAN = "ru"
    UKRAINIAN = "uk"
    HINDI = "hi"
    THAI = "th"
    CHINESE_CHINA = "zh-CN"
    JAPANESE = "ja"
    CHINESE_TAIWAN = "zh-TW"
    KOREAN = "ko"


class Localization:
    def __init__(self, locale: Locale, value: str):
        self.locale = locale
        self.value = value

    def to_dict(self) -> Dict[str, str]:
        return {self.locale.value: self.value}
