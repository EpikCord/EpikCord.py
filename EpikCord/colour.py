from typing import (
    Tuple,
    Type,
    TypeVar,
    Any
)

CT = TypeVar("CT", bound="Colour")


class Colour:
    # Some of this code is sourced from discord.py, rest assured all the
    # colors are different from discord.py
    __slots__ = ("value",)

    def __init__(self, value: int):
        if not isinstance(value, int):
            raise TypeError(
                f"Expected int parameter, received {value.__class__.__name__} instead."
            )

        self.value: int = value

    def _get_byte(self, byte: int) -> int:
        return (self.value >> (8 * byte)) & 0xFF

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Colour) and self.value == other.value

    def __ne__(self, other: Any) -> bool:
        return not self.__eq__(other)

    def __str__(self) -> str:
        return f"#{self.value:0>6x}"

    def __int__(self) -> int:
        return self.value

    def __repr__(self) -> str:
        return f"<Colour value={self.value}>"

    def __hash__(self) -> int:
        return hash(self.value)

    @property
    def r(self) -> int:
        """Return the red component in rgb"""
        return self._get_byte(2)

    @property
    def g(self) -> int:
        """Return the green component in rgb"""
        return self._get_byte(1)

    @property
    def b(self) -> int:
        """Return the blue component in rgb"""
        return self._get_byte(0)

    def to_rgb(self) -> Tuple[int, int, int]:
        """Returns a rgb color as a tuple"""
        return self.r, self.g, self.b

    @classmethod
    def from_rgb(cls: Type[CT], r: int, g: int, b: int) -> CT:
        """Constructs a :class:`Colour` from an RGB tuple."""
        return cls((r << 16) + (g << 8) + b)

    @classmethod
    def lime_green(cls: Type[CT]) -> CT:
        """Returns a color of lime green"""
        return cls(0x00FF01)

    @classmethod
    def light_green(cls: Type[CT]) -> CT:
        """Returns a color of light green"""
        return cls(0x00FF22)

    @classmethod
    def dark_green(cls: Type[CT]) -> CT:
        """Returns a color of dark green"""
        return cls(0x00570A)

    @classmethod
    def light_blue(cls: Type[CT]) -> CT:
        """Returns a color of light blue"""
        return cls(0x00FF01)

    @classmethod
    def dark_blue(cls: Type[CT]) -> CT:
        """Returns a color of dark blue"""
        return cls(0x0A134B)

    @classmethod
    def light_red(cls: Type[CT]) -> CT:
        """Returns a color of light red"""
        return cls(0xAA5B54)

    @classmethod
    def dark_red(cls: Type[CT]) -> CT:
        """Returns a color of dark red"""
        return cls(0x4C0000)

    @classmethod
    def black(cls: Type[CT]) -> CT:
        """Returns a color of black"""
        return cls(0x000000)

    @classmethod
    def white(cls: Type[CT]) -> CT:
        """Returns a color of white"""
        return cls(0xFFFFFF)

    @classmethod
    def lightmode(cls: Type[CT]) -> CT:
        """Returns the color of the background when the color theme in
        Discord is set to light mode. An alias of `white`"""
        return cls(0xFFFFFF)

    @classmethod
    def darkmode(cls: Type[CT]) -> CT:
        """Returns the color of the background when the color theme in
        Discord is set to dark mode"""
        return cls(0x363940)

    @classmethod
    def amoled(cls: Type[CT]) -> CT:
        """Returns the color of the background when the color theme in
        Discord is set to amoled mode. An alias of `black`"""
        return cls(0x000000)

    @classmethod
    def blurple_old(cls: Type[CT]) -> CT:
        """Returns the old Discord Blurple color"""
        return cls(0x7289DA)

    @classmethod
    def blurple_new(cls: Type[CT]) -> CT:
        """Returns the new Discord Blurple color"""
        return cls(0x5865F2)

    default = black


Color = Colour

