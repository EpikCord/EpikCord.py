<p align="center">
    <img alt="EpikCord logo" src="docs/EpikCord_Logo.png" width="200"> <!-- Yes I sourced this from DiscordGO because their design inspired me :D-->
</p>

## EpikCord.py

`Important note:  The library is currently undergoing a rewrite. The library will be back soon`

EpikCord.py is an **API wrapper for discord** that aims to be very customizable and easy to use.

## Why EpikCord.py?
Unlike most libraries, Most of the classes in EpikCord.py have the data attribute. This means that you can hack and customize the class to your liking.

However, this library is not recommended for beginner users.

## Contributing to the library
We love contributions that help us, so feel free to! You won't be rewarded for this, but it helps us and we'd be very pleased with any contribution.
See the [Contributing](./CONTRIBUTING.md) page for more information.

## Installing

Requirements = **Python 3.8 or more**

For installing base library:

``` sh
#Windows
py -3.8 -m pip install epikcord.py
#Linux/Mac
python3 -m pip install epikcord.py
```

For installing voice support (optional[uses [PyNaCl](https://pypa.org/project/pynacl/)]):

``` sh
#Windows
py -3.8 -m pip install epikcord.py[voice]
#Linux/Mac
python3 -m pip install epikcord.py[voice]
```

For installing the library directly from the GitHub repository(requires [git](https://git-scm.com/downloads)):


``` sh
#Windows
py -3.8 -m pip install git+https://github.com/EpikCord/EpikCord.py
#Linux/Mac
python3 -m pip install git+https://github.com/EpikCord/EpikCord.py
```

## Examples
All examples are located in the [examples](./examples) folder.
Main ones are:
* [Basic Bot Example](./examples/basic_bot.py)
* [Basic Command Example](./examples/message.py)
* [Slash Command Example](./examples/slash_commands.py)
* [User Command Example](./examples/user_commands.py)
* [Message Command Example](./examples/message_commands.py)

## Important links
Documentation - [here](https://epikcord-guide.vercel.app/)

Discord Server for assistance - [here](https://discord.gg/4R473R73kQ)

All Examples - [here](./examples)





