from .type_enums import Locale


class Localization:
    def __init__(self, locale: Locale, value: str):
        self.locale: Locale = str(locale)
        self.value: str = value

    def to_dict(self):
        return {self.locale: self.value}


Localisation = Localization

__all__ = ("Localization", "Localisation")
