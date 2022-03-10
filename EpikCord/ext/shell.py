
import platform
import subprocess
import asyncio
from  logging import getLogger
from ..__init__ import Client, TextBasedChannel
from typing import (Optional, List, Tuple)
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
        self.system_shell:List[str] = shells[self.system]
        self.proc = ""
        self.client:Client = client
        self.owners:List = client.is_owner() if client.is_owner is not [] else owner_ids
        if self.owners == []:
            raise CWE78Error("As a security measure, we are preventing you to do this without owner ids.\nThis is because allowing could make arbitrary code execution possible")
        LogHandler.info("Finding Terminal!")
        if self.system == "windows":
            for shell in self.system_shell:
                check_sequence = [shell, "\c", "echo", "EpikCord shell is ready"]
                run_test = subprocess.Popen(check_sequence)
                if run_test.returncode == 0:
                    LogHandler.info("Success! Terminal Found")
                    self.shell:str = shell 
                    self.sequence = [shell, "/c"]
        else:
            raise OSNotSupportedError(f"The os provided,{self.system} is not supported")
        
    async def ShellListener(self, channel:TextBasedChannel):
        owners = self.owners
        while True:
            resp = await self.client.wait_for("message_create")
            if resp.channel.id == channel.id:
                for owner in owners:
                    if resp.member.id == owner:
                        self.sequence.append(resp.content)
                        self.proc = await asyncio.create_subprocess_exec(self.sequence)
                        #set up listener 
                        

    def Communicate(self, communication):
        outs, errs = await self.proc.communicate(communication)
        try:
            outs = str(outs)
            errs = str(errs)
        except:
            pass
        return outs,errs




        