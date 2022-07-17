__all__ = ("__version__", "info")

__version__ = "0.5.2"


def info():
    print(
        f"Version {__version__} of EpikCord.py, written by the organization EpikCord. "
        "This is an unstable build and may contain bugs. "
        "Please report any bugs to https://github.com/EpikCord/EpikCord.py/issues."
    )


if __name__ == "__main__":
    info()
