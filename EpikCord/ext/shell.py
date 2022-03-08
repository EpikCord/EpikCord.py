import platform
import subprocess
import asyncio
from  logging import getLogger
from ..__init__ import Client
from typing import (Optional, List)
LogHandler = getLogger("EpikCord.ext.shell")
#contains shell paths. TODO:Add more windows terminals

shells = {
    "windows": ["C:\\Windows\\cmd.exe"]
}

class ShellHandler:
    def __init__(self, client:Client, owner_ids:Optional[List[str]]) ->None:
        self.system:str = platform.system()
        self.system_shells:List[str] = shells[self.system]
        LogHandler.info("Finding Terminal!")
        if self.system == "windows":
            for shell in self.system_shells:
                check_sequence = [shell, "\c", "echo", "EpikCord shell is ready"]
                run_test = subprocess.Popen(check_sequence)
                if run_test.returncode == 0:
                    LogHandler.info("Success! Terminal Found")
                    self.shell_path = shell

            #validation for each shell

        