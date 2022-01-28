# Install Epikcord.py

## Requirements

The minimal requirements for EpikCord.py is `Python>=3.8`. Python 3.7 and lower and Python 2 family are not supported

## Install
**Warning!!**<Br>
This Library is in preview and hasnt been released yet. Some features may not work properly.

Get the library from the Python Package Index (PyPI)
<br>
```
pip install EpikCord.py
```

### Install in an Virtual Environment (venv)

Sometimes you might want to keep this library from conflicting with other libraries or use a different version of libs than the ones in the system.You also might not have permissions for installing libraries. Luckily Virtual Environments are here to save you. From Python3.3 ,there is a concept called Virtual Environment to help maintain these libs


#### For the quick and dirty:

1. Go to your project working directory:

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
