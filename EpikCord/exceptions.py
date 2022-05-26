class EpikCordException(Exception):
    ...


class InvalidApplicationCommandType(EpikCordException):
    ...


class InvalidApplicationCommandOptionType(EpikCordException):
    ...


class InvalidOption(EpikCordException):
    ...


class InvalidStatus(EpikCordException):
    ...


class ClosedWebSocketConnection(EpikCordException):
    ...


class MissingClientSetting(EpikCordException):
    ...


class MissingCustomId(EpikCordException):
    ...


class DiscordAPIError(EpikCordException):
    ...


class InvalidData(EpikCordException):
    ...


class InvalidIntents(EpikCordException):
    ...


class ShardingRequired(EpikCordException):
    ...


class InvalidToken(EpikCordException):
    ...


class UnhandledEpikCordException(EpikCordException):
    ...


class DisallowedIntents(EpikCordException):
    ...


class BadRequest400(EpikCordException):
    ...


class Unauthorized401(EpikCordException):
    ...


class Forbidden403(EpikCordException):
    ...


class NotFound404(EpikCordException):
    ...


class MethodNotAllowed405(EpikCordException):
    ...


class Ratelimited429(EpikCordException):
    ...


class GateawayUnavailable502(EpikCordException):
    ...


class InternalServerError5xx(EpikCordException):
    ...


class TooManyComponents(EpikCordException):
    ...


class InvalidComponentStyle(EpikCordException):
    ...


class CustomIdIsTooBig(EpikCordException):
    ...


class InvalidArgumentType(EpikCordException):
    ...


class TooManySelectMenuOptions(EpikCordException):
    ...


class LabelIsTooBig(EpikCordException):
    ...


class ThreadArchived(EpikCordException):
    ...


class FailedToConnectToVoice(EpikCordException):
    ...


class FailedCheck(EpikCordException):
    ...
