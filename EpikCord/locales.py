from typing import Dict
from .utils import Locale


class Localization:
    def __init__(self, locale: Locale, value: str):

        self.locale = locale
        self.value = value

    def to_dict(self) -> Dict[str, str]:
        return {self.locale.value: self.value}
