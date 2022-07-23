import argparse
import colorama


__all__ = ("__version__", "info")
__version__ = "0.5.2"
_bot_tmplate = """#!/usr/bin/env python
from EpikCord import Client, Intents

intents = Intents.all()

client: Client = Client([token], intents)


@client.event()
async def ready():
    print("Ready!")
# Write commands here

client.login()
"""
win_restricted = (
    "CON",
    "CON1",
    "CON2",
    "CON3",
    "CON4",
    "CON5",
    "CON6",
    "CON7",
    "CON8",
    "CON9",
    "AUX",
    "AUX1",
    "AUX2",
    "AUX3",
    "AUX4",
    "CON5",
    "CON6",
    "CON7",
    "CON8",
    "CON9",

)

parser = argparse.ArgumentParser()
parser.add_argument(
    "--version", help="displays the version of the library", action="store_true"
)
colorama.init(autoreset=True)


def setup():
    print(f"{colorama.Back.RED}{colorama.Fore.BLUE}Welcome To Setup!")
    name_query = input("What is the name of the new bot: ")

    ...


def info():
    print(
        f"Version {__version__} of EpikCord.py, written by the organization EpikCord. "
        "This is an unstable build and may contain bugs. "
        "Please report any bugs to https://github.com/EpikCord/EpikCord.py/issues."
    )


def parse_args(args: argparse.ArgumentParser):
    args = parser.parse_args()
    if args.version:
        info()
    else:
        setup()


def main():

    parse_args(parser)


if __name__ == "__main__":
    main()
