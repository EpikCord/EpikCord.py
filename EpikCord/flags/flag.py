from typing import (
    Any,
    TYPE_CHECKING
)


class Flag:
    if TYPE_CHECKING:
        class_flags: "dict[str, Any]"

    def __init_subclass__(cls) -> None:
        cls.class_flags = {k: v for k, v in cls.__dict__.items() if isinstance(v, int)}
        return cls

    def __init__(self, value: int = 0, **kwargs):
        self.value = value
        self.turned_on: "list[str]" = [k for k, a in kwargs.items() if a]

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