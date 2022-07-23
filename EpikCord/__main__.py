import argparse
from ast import parse

__all__ = ("__version__", "info")

__version__ = "0.5.2"

parser = argparse.ArgumentParser()
parser.add_argument("--version", help="displays the version of the library", action='store_true')
parser.add_argument("bot")




def info():
    print(
        f"Version {__version__} of EpikCord.py, written by the organization EpikCord. "
        "This is an unstable build and may contain bugs. "
        "Please report any bugs to https://github.com/EpikCord/EpikCord.py/issues."
    )

def parse_args(args:argparse.Namespace):
    if args.version:
        info()

def main():
    args = parser.parse_args()
    parse_args(args)