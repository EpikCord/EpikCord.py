__all__ = ("__version__", "info")
from ..EpikCord import __version__


def info():
    print(
        f"Version {__version__} of EpikCord.py, written by EpikHost. "
        "This is an unstable build and will contain bugs. "
        "Please report any bugs to https://github.com/EpikCord/EpikCord.py/issues."
    )


if __name__ == "__main__":
    info()
