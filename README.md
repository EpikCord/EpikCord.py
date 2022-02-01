# EpikCord.py
Welcome to EpikCord.py!
This is an API Wrapper for Discord's API for Python!
We've decided not to fork discord.py and start completely from scratch for a new, better structuring system!

## Why EpikCord.py?
Because Discord.py has been discontinued and is no longer maintained, we've decided to make our own Python API Wrapper for the Discord API.
The reason for this is because we want an easier method for you, the developer, to use the API, with great ease.

## Why is there literally nothing in here?
Here, we decided to ***not*** for Discord.py and to go for an entirely different structure to our code, thus meaning we're not gonna have anywhere to start from.
We may include a series on the EpikHost YouTube channel for helping people migrate to our library from Discord.py (not promised).

## I want to contribute!
We love contributions that help us, so feel free to! You won't be rewarded for this, but it helps us and we'd be very pleased with any contribution.
See [Contributing.md](./Contributing.md) for more information.

## Where are your docs?
SoonTM

## Why doesn't it work?
We plan on launching a 1.0 version which will work, until that comes out you just have to sit and look at the code and predict what functions are gonna come out next.

## I need help!
If you need help, you can join our [EpikCord.py Discord Server](https://discord.gg/4R473R73kQ) and ask for help there.

<a href="https://discord.gg/4R473R73kQ" target="_blank" rel="noopener noreferrer">
    <img src="https://img.shields.io/discord/937364424208039957?color=9cf&logo=discord&label=discord" alt="Discord server">
</a>

# Installing Epikcord.py

## Requirements

The minimal requirements for EpikCord.py is `Python>=3.8`. Python 3.7 and lower and Python 2 family are not supported

## Install
**Warning!**<Br>
This Library is in preview and hasn't been released yet. Some features may not work properly.

Get the library from the Python Package Index (PyPI)
<br>
```
pip install EpikCord.py
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
> For Linux/MacOS
> ```sh
>  $ source YourBotEnvName/bin/activate
> ```
> For Windows:
> ```
>  $ YourBotEnvName\Scripts\activate.ps1
> ```

3. Use pip as usual!
> ``` sh
> pip install -U EpikCord.py
> ```

Congrats! Your venv is all set up!
