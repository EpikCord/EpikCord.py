import argparse
import os
import re
import sys
import colorama
from platform import system as get_parent_os

from EpikCord import __version__
_bot_tmplate = """#!/usr/bin/env python
from EpikCord import Client, Intents
from config import token
class [name]Client(Client):

    def __init__(self):
        super().__init__()

    #[_section]
    
intents = Intents.all()

client: [name]Client = [name]Client(token, intents)


@client.event()
async def ready():
    print("Ready!")
# Write commands here

client.login()
"""
__gitignore_template = """# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class
# C extensions
*.so
# Distribution / packaging
.Python
env/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
*.egg-info/
.installed.cfg
*.egg
# Our configuration files
config.py
"""
__config_file_template = """
token = [token]
"""
if get_parent_os().lower() == "windows":
    IS_WINDOWS = True
else:
    IS_WINDOWS = False


class InvalidNameError(Exception):
    ...




parser = argparse.ArgumentParser()
parser.add_argument(
    "--version", help="displays the version of the library", action="store_true"
)
parser.add_argument("-n","--new", help="Creates an new bot", action='store_true')

colorama.init(autoreset=True)

def get_question(name_query):
        directory = input(
            "Which directory to write the bot to?:(Type . to make a bot in the current directory): "
        )
        if not os.path.isdir(directory) or directory != ".":
            dir_question = input(
                "This directory does not exist. Would you like me to create it?(y/n)"
            )
            if dir_question == "y" :
                os.makedirs(f"{directory}/{name_query}")
                directory = f"{directory}/{name_query}"
            else:
                sys.exit("OK, Exiting...")
        elif directory == ".":
            directory = os.getcwd()
            os.makedirs(f"{directory}/{name_query}")
            directory = f"{os.getcwd()}/{name_query}"
        print("We need to ask you a few questions, then we will finish the setup")
        token = input("What is the token for this bot?: ")
        gitignore_confirm = input("Would you like to add a .gitignore file to the folder(y/n):")
        section_confirm = input("Add a sections folder?")
        print("Writing the bot to the current directory")
        return directory,token, gitignore_confirm,section_confirm

def write_bot(name,folder,token,gitignore,if_sections):
    if gitignore == 'y':
        with open(f"{folder}/.gitignore", 'x') as write_file:
            write_file.write(__gitignore_template)
    if if_sections == 'y':
        os.makedirs(f"{folder}/sections")
        print('Sections are not yet supported properly')
    with open(f"{folder}/{name}.py", 'x') as write_file:
        write_file.write(_bot_tmplate.replace('[name]', name))
    with open(f"{folder}/config.py", 'x') as write_file:
        write_file.write(__config_file_template.replace('[token]', f"\'{token}\'"))

    

def setup():
    if IS_WINDOWS:
        print(f"{colorama.Back.GREEN}{colorama.Fore.BLUE}Welcome To Setup!")
        name_query = input("What is the name of the new bot: ") or "DefaultBot"
        
        if re.fullmatch(r'((AUX|CON|LPT)\d?)|NUL|PRN', name_query.upper()):
            raise InvalidNameError(
                    "This is a Windows reserved keyword, You are not allowed to create these files"
                )
        directory,token, gitignore_confirm, section_confirm=get_question(name_query)
        write_bot(name_query,directory,token,gitignore_confirm, section_confirm)
    else:
        print(f"{colorama.Back.GREEN}{colorama.Fore.BLUE}Welcome To Setup!")
        name_query = input("What is the name of the new bot: ") or "DefaultBot"
        directory,token, gitignore_confirm, section_confirm=get_question(name_query)
        write_bot(name_query,directory,token,gitignore_confirm, section_confirm)


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
    elif args.new:
        setup()
    else:
        print("Error: Program called with no switches")
        parser.print_help()
        parser.exit(0)


def main():

    parse_args(parser)


if __name__ == "__main__":
    main()
