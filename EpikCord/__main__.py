import argparse
import os
import sys
import colorama
from platform import system as get_parent_os

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
if get_parent_os().lower() == "windows":
    IS_WINDOWS = True
else:
    IS_WINDOWS = False


class InvalidNameError(Exception):
    ...


win_reserved = (
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
    "PRN",
    "NUL",
    "AUX",
    "LPT1",
    "LPT2",
    "LPT3",
    "LPT4",
    "LPT5",
    "LPT6",
    "LPT7",
    "LPT8",
    "LPT9",
)

parser = argparse.ArgumentParser()
parser.add_argument(
    "--version", help="displays the version of the library", action="store_true"
)
colorama.init(autoreset=True)


def write_bot(token):
    if IS_WINDOWS:
        ...


def setup():
    if IS_WINDOWS:
        print(f"{colorama.Back.GREEN}{colorama.Fore.BLUE}Welcome To Setup!")
        name_query = input("What is the name of the new bot: ")
        for name in win_reserved:
            if name_query.upper() == name:
                raise InvalidNameError(
                    "This is a Windows reserved keyword, You are not allowed to create these files"
                )
        directory = input(
            "Which directory to write the bot to?:(Type current to make a bot in the current directory): "
        )
        if not os.path.isdir(directory) or directory == "current":
            dir_question = input(
                "This directory does not exist. Would you like me to create it?(y/n)"
            )
            if not dir_question == "y":
                sys.exit("OK, Exiting...")
        print("We need to ask you a few questions, then we will finish the setup")
        token = input("What is the token for this bot?: ")
        print("Writing the bot to the current directory")
        write_bot(token)
    else:
        print(f"{colorama.Back.GREEN}{colorama.Fore.BLUE}Welcome To Setup!")
        name_query = input("What is the name of the new bot: ")
        directory = input(
            "Which directory to write the bot to?:(Type current to make a bot in the current directory): "
        )
        if not os.path.isdir(directory) or directory == "current":
            dir_question = input(
                "This directory does not exist. Would you like me to create it?(y/n)"
            )
            if not dir_question == "y":
                sys.exit("OK, Exiting...")
        print("We need to ask you a few questions, then we will finish the setup")
        token = input("What is the token for this bot?: ")
        print("Writing the bot to the current directory")
        write_bot(token)


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
