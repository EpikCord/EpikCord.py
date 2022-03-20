from typing import Optional, List,Union


from EpikCord import *

class SectionNotFound(Exception):
    ...


class Section:
    def __init__(self):
        self.commands = {}
        self.events = {}
    
    __Section_name__:str

    def event(self, event_name: str):
        def register_event(func):
            self.events[event_name] = func
        return register_event

    def slash_command(self, *, name: str, description: Optional[str], options: List[Union[Subcommand, SubCommandGroup, StringOption, IntegerOption, BooleanOption, UserOption, ChannelOption, RoleOption, MentionableOption, NumberOption]]):
        def register_slash_command(func):
            self.commands[name] = {
                "callback": func,
                "name": name,
                "description": description,
                "options": options
            }
        return register_slash_command

    def get_commands(self) -> List[Union[SlashCommand,ClientUserCommand,ClientMessageCommand]]:

        return [c for c in self.commands]

    def command_unload(self, name:str):
        try:
            self.commands.pop(name)
        except KeyError:
            raise SectionNotFound("Error: Section already unloaded or does not exist")

    def command_reload(self, name:str):
        ... #TODO: Implement reload

    
