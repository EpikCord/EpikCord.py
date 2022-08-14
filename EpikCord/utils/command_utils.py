from ..client import CommandHandler

class CommandUtils(CommandHandler):
    @staticmethod
    def check(callback):
        from EpikCord import Check

        return Check(callback)

    @staticmethod
    def event(name: str):
        from EpikCord import Event

        def wrapper(callback):
            return Event(callback, event_name=name)

        return wrapper