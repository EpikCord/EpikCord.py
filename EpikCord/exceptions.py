from dataclasses import dataclass


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


@dataclass
class LocatedError:
    code: str
    message: str
    path: str


class DiscordAPIError(EpikCordException):
    def __init__(self, body):
        self.body = body
        self.code = body.get("code")
        self.message = body.get("message")
        self.errors = body.get("errors")
        self.errors_list = self.extract_errors(self.errors)

        super().__init__(
            "\n".join(
                f"{e.path} - {e.code} - {e.message}"
                for e in self.errors_list
            )
        )

    def extract_errors(self, d, key_path=None):
        """Get _errors key from the given dictionary."""
        if key_path is None:
            key_path = []

        if "_errors" in d:
            return [
                LocatedError(**error, path='.'.join(key_path[1:]))
                for error in d["_errors"]
            ]

        return [
            x for k, v in d.items() if isinstance(v, dict)
            for x in self.extract_errors(v, key_path + [k])
        ]


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


class t(EpikCordException):
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
