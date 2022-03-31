class EpikCordException(Exception):
    """
    Base exception for EpikCord.
    """
    ...


class MissingCustomId(EpikCordException):
    """
    Raised when you don't input a custom_id for a component.
    """
    ...

class MissingClientSetting(EpikCordException):
    """
    Raised when you don't input a setting for Client.
    """
    ...


class ClosedWebSocketConnection(EpikCordException):
    """
    Raised when the websocket connection is closed.
    """
    ...


class InvalidStatus(EpikCordException):
    """
    Raised when you try to set an invalid Status.
    """
    ...

class InvalidApplicationCommandType(EpikCordException):
    """
    Raised when you try to set an invalid ApplicationCommand type.
    """
    ...

class InvalidApplicationCommandOptionType(EpikCordException):
    """
    Raised when you try to set an invalid ApplicationCommandOption type.
    """
    ...

class DiscordAPIError(EpikCordException):
    """
    Raised when an error is returned from the Discord API.
    """
    ...


class InvalidData(EpikCordException):
    """
    Raised when invalid data is sent to Discord.
    """
    ...


class InvalidIntents(EpikCordException):
    """
    Raised when you try to set invalid Intents
    """
    ...


class ShardingRequired(EpikCordException):
    """
    Raised when you must shard your bot.
    """
    ...


class InvalidToken(EpikCordException):
    """
    Raised when you try to set an invalid token.
    """
    ...

class DisallowedIntents(EpikCordException):
    """
    Raised when the intents you tried to set are not allowed for you bot.
    """
    ...

class TooManyComponents(EpikCordException):
    """
    Raised when you have too many Component in an ActionRow
    """
    ...


class InvalidComponentStyle(EpikCordException):
    """
    Raised when you try to set an invalid style for a component.
    """
    ...


class CustomIdIsTooBig(EpikCordException):
    """
    Raised when your custom_id is too big."""
    ...


class InvalidArgumentType(EpikCordException):
    """
    Raised when your argument type is invalid.
    """
    ...

class TooManySelectMenuOptions(EpikCordException):
    """
    Raised when you try to set too many SelectMenuOptions for a SelectMenu.
    """
    ...


class LabelIsTooBig(EpikCordException):
    """
    Raised when your label is too big.
    """
    ...


class ThreadArchived(EpikCordException):
    """
    Raised when you try to send a message to an archived thread.
    """
    ...

class InvalidOption(EpikCordException):
    ...
