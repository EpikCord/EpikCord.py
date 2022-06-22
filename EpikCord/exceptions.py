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
    def __init__(self, body):
        self.body = body
        self.code = body["code"]
        self.message = body["message"]
        self.errors = body.get("errors")
        self.errors_list = self.extract_errors(self.errors)
        final_message = ""
        for error in self.errors_list:
            final_message += f"{error['path']} - {error['code']} - {error['message']}\n"
        super().__init__(final_message)

    def extract_errors(self, d, key_path=None):
        """Get _errors key from the given dictionary."""
        if key_path is None:
            key_path = []

        if "_errors" in d:
            errors = []
            for error in d["_errors"]:
                error["path"] = '.'.join(key_path[1:])
                errors.append(error)
            return errors

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


class Unauthorized401(DiscordAPIError):
    ...


class Forbidden403(DiscordAPIError):
    ...


class NotFound404(DiscordAPIError):
    ...


class MethodNotAllowed405(DiscordAPIError):
    ...


class Ratelimited429(DiscordAPIError):
    ...


class GateawayUnavailable502(DiscordAPIError):
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
