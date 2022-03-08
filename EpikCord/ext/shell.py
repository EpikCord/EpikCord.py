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
class CWE78Error(Exception):
    ...
class OSNotSupportedError(Exception):
    ...

class ShellHandler:
    """_summary_
    """    
    def __init__(self, client:Client, owner_ids:Optional[List[str]]) ->None:
        self.system:str = platform.system()
        self.shell:List[str] = shells[self.system]
        self.owners = client.is_owner() if client.is_owner is not [] else owner_ids
        if self.owners == []:
            raise CWE78Error("As a security measure, we are preventing you to do this without owner ids.\nThis is because allowing could make arbitary code exection possible")
        LogHandler.info("Finding Terminal!")
        if self.system == "windows":
            for shell in self.shell:
                check_sequence = [shell, "\c", "echo", "EpikCord shell is ready"]
                run_test = subprocess.Popen(check_sequence)
                if run_test.returncode == 0:
                    LogHandler.info("Success! Terminal Found")

            #validation for each shell

        