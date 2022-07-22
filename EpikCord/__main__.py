import argparse

__all__ = ("__version__", "info")

__version__ = "0.5.2"

class F:
    ...
parser = argparse.ArgumentParser()
parser.add_argument("--version", help="displays the version of the library",nargs="?")
args = parser.parse_args(namespace=F)




def info():
    print(
        f"Version {__version__} of EpikCord.py, written by the organization EpikCord. "
        "This is an unstable build and may contain bugs. "
        "Please report any bugs to https://github.com/EpikCord/EpikCord.py/issues."
    )


if args.version:
    print("lol")
