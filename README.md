<p align="center">
    <img alt="EpikCord logo" src="docs/EpikCord_Logo.png" width="200"> <!-- Yes I sourced this from DiscordGO because their design inspired me :D-->
</p>


[![Discord server](https://img.shields.io/discord/937364424208039957?color=9cf&logo=discord&label=discord&style=for-the-badge)](https://discord.gg/4R473R73kQ)
[![Documentation Status](https://readthedocs.org/projects/epikcordpy/badge/?version=latest&style=for-the-badge)](https://epikcordpy.readthedocs.io/en/latest/?badge=latest)

# EpikCord.py
Welcome to EpikCord.py!
This is an API Wrapper for Discord's API, made in Python!
We've decided not to fork discord.py and start completely from scratch for a new, better structuring system!

## Why EpikCord.py?
There are many other libraries for the Discord API written in Python, there is no reason for you to choose us over other great libraries, however we are in active development and constantly releasing new features very often, we're also built from the ground up rather than most of the other libraries, which are forks of Discord.py.

## I want to contribute!
We love contributions that help us, so feel free to! You won't be rewarded for this, but it helps us and we'd be very pleased with any contribution.
See the [Contributing](./CONTRIBUTING.md) page for more information.

## Where are your docs?
Have functions and attributes you are not sure about? Check our docs [here](https://epikcord-guide.vercel.app/)

## I need help!
If you need help, you can join our [EpikCord.py Discord Server](https://discord.gg/4R473R73kQ) and ask for help there.

# Installing Epikcord.py

## Requirements

The minimal requirements for EpikCord.py are`Python>=3.8`. Python 3.7 and lower and the Python 2 family are not supported at all and we will not provide support for issues involving them.

## Install
**Warning!**<Br>
This Library is in preview and hasn't been released yet. Some features may not work properly.

Get the library from the Python Package Index (PyPI)
<br>

```
pip install EpikCord.py
```

Or use git to get the development version with the latest features!

```sh
pip install git+https://github.com/EpikHost/EpikCord.py
```

### Install in an Virtual Environment (venv)

Sometimes you might want to keep this library from conflicting with other libraries or use a different version of libs than the ones in the system. You also might not have permissions for installing libraries. Luckily Virtual Environments are here to save you. From Python3.3, there is a concept called Virtual Environment to help maintain these libs


#### For the quick and dirty:

1. Go to your project's working directory:

> ``` sh
>  $ cd bot-source-dir
>  $ python3 -m venv YourBotEnvName
> ```

2. Activate the venv
If you don't know how to see it [here](https://docs.python.org/3/library/venv.html)

3. Installing
> ``` sh
> pip install -U EpikCord.py
> ```

# Examples

Basic bot example- [here](./examples/basic_bot.py)
Message command example - [here](./examples/message_commands.py)
Slash command example - [here](./examples/slash_commands.py)
User Commands example - [here](./examples/user_commands.py)


