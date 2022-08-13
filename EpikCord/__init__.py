"""
NOTE: version string only in setup.cfg
"""
from __future__ import annotations

import datetime
from typing import Optional, List, Union, TypeVar

from .client import *
from .managers import *
from .abstract import *
from .auto_moderation import *
from .application import *
from .channels import *
from .close_event_codes import *
from .colour import *
from .mentioned import *
from .components import *
from .exceptions import *
from .flags import *
from .localizations import *
from .message import *
from .sharding import *
from .opcodes import *
from .user import *
from .options import *
from .partials import *
from .rtp_handler import *
from .guild import *
from .voice import *
from .status_code import *
from .sticker import *
from .thread import *
from .presence import *
from .type_enums import *
from .utils import *
from .commands import *
from .webhooks import *
from .interactions import *

T = TypeVar("T")
logger = getLogger(__name__)

__version__ = "0.5.2"

"""
:license:
Some parts of the code is sourced from discord.py
The MIT License (MIT)
Copyright © 2015-2021 Rapptz
Copyright © 2021-present EpikHost
Permission is hereby granted, free of charge, to any person obtaining a copy of 
this software and associated documentation files (the “Software”), to deal in 
the Software without restriction, including without limitation the rights to 
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies 
of the Software, and to permit persons to whom the Software is furnished to do 
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all 
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, RESS OR IMPLIED,
 INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A 
 PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR 
 COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER 
 IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN 
 CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE."""

# class ClientGuildMember(Member):
#     def __init__(self, client: Client,data: dict):
#         super().__init__(data)

class Invite:
    def __init__(self, data: dict):
        self.code: str = data.get("code")
        self.guild: Optional[PartialGuild] = (
            PartialGuild(data.get("guild")) if data.get("guild") else None
        )
        self.channel: GuildChannel = (
            GuildChannel(data.get("channel")) if data.get("channel") else None
        )
        self.inviter: Optional[User] = (
            User(data.get("inviter")) if data.get("inviter") else None
        )
        self.target_type: int = data.get("target_type")
        self.target_user: Optional[User] = (
            User(data.get("target_user")) if data.get("target_user") else None
        )
        self.target_application: Optional[Application] = (
            Application(data.get("target_application"))
            if data.get("target_application")
            else None
        )
        self.approximate_presence_count: Optional[int] = data.get(
            "approximate_presence_count"
        )
        self.approximate_member_count: Optional[int] = data.get(
            "approximate_member_count"
        )
        self.expires_at: Optional[str] = data.get("expires_at")
        self.stage_instance: Optional[GuildStageChannel] = (
            GuildStageChannel(data.get("stage_instance"))
            if data.get("stage_instance")
            else None
        )
        self.guild_scheduled_event: Optional[GuildScheduledEvent] = GuildScheduledEvent(
            data.get("guild_scheduled_event")
        )



class AllowedMention:
    def __init__(
        self,
        allowed_mentions: List[str],
        replied_user: bool,
        roles: List[str],
        users: List[str],
    ):
        self.allowed_mentions: List[str] = allowed_mentions
        self.replied_user: bool = replied_user
        self.roles: List[str] = roles
        self.users: List[str] = users

    def to_dict(self) -> Dict[str, Any]:
        return {
            "allowed_mentions": self.allowed_mentions,
            "replied_user": self.replied_user,
            "roles": self.roles,
            "users": self.users,
        }


class SlashCommand(ApplicationCommand):
    def __init__(self, data: dict):
        super().__init__(data)
        self.options: Optional[List[AnyOption]] = data.get("options")
        opts = [
            Subcommand,
            SubCommandGroup,
            StringOption,
            IntegerOption,
            BooleanOption,
            UserOption,
            ChannelOption,
            RoleOption,
            MentionableOption,
            NumberOption,
            AttachmentOption,
        ]

        for option in self.options:
            option_type = option.get("type")
            if option_type >= len(opts):
                raise ValueError(f"Invalid option type {option_type}")

            option.pop("type")
            opts[option_type - 1](**option)

    def to_dict(self):
        json_options = [option.to_dict for option in self.options]
        return {
            "name": self.name,
            "type": self.type,
            "description": self.description,
            "options": json_options,
        }


__all__ = (
    "__version__",
    "ActionRow",
    "Activity",
    "AllowedMention",
    "AnyChannel",
    "AnyOption",
    "Application",
    "ApplicationCommand",
    "ApplicationCommandInteraction",
    "ApplicationCommandOption",
    "ApplicationCommandPermission",
    "ApplicationCommandSubcommandOption",
    "Attachment",
    "AttachmentOption",
    "AutoCompleteInteraction",
    "AutoModerationAction",
    "AutoModerationActionMetaData",
    "AutoModerationActionType",
    "AutoModerationEventType",
    "AutoModerationKeywordPresetTypes",
    "AutoModerationRule",
    "AutoModerationTriggerMetaData",
    "AutoModerationTriggerType",
    "BaseChannel",
    "BaseCommand",
    "BaseComponent",
    "BaseInteraction",
    "BaseSlashCommandOption",
    "BooleanOption",
    "Bucket",
    "Button",
    "ButtonStyle",
    "CacheManager",
    "ChannelCategory",
    "ChannelManager",
    "ChannelOption",
    "ChannelTypes",
    "Check",
    "Client",
    "ClientApplication",
    "ClientMessageCommand",
    "ClientSlashCommand",
    "ClientUser",
    "ClientUserCommand",
    "Color",
    "Colour",
    "CommandUtils",
    "Connectable",
    "CustomIdIsTooBig",
    "DMChannel",
    "DisallowedIntents",
    "DiscordAPIError",
    "DiscordGatewayWebsocket",
    "DiscordWSMessage",
    "Embed",
    "Emoji",
    "EpikCordException",
    "Event",
    "EventHandler",
    "FailedCheck",
    "FailedToConnectToVoice",
    "File",
    "Flag",
    "Forbidden403",
    "GateawayUnavailable502",
    "GatewayCECode",
    "GatewayOpcode",
    "Guild",
    "GuildApplicationCommandPermission",
    "GuildBan",
    "GuildChannel",
    "GuildManager",
    "GuildMember",
    "GuildNewsChannel",
    "GuildNewsThread",
    "GuildPreview",
    "GuildScheduledEvent",
    "GuildStageChannel",
    "GuildTextChannel",
    "GuildWidget",
    "GuildWidgetSettings",
    "HTTPClient",
    "IntegerOption",
    "Integration",
    "IntegrationAccount",
    "Intents",
    "InvalidApplicationCommandOptionType",
    "InvalidApplicationCommandType",
    "InvalidArgumentType",
    "InvalidComponentStyle",
    "InvalidData",
    "InvalidIntents",
    "InvalidOption",
    "InvalidStatus",
    "InvalidToken",
    "Invite",
    "LabelIsTooBig",
    "Locale",
    "Localisation",
    "Localization",
    "LocatedError",
    "MentionableOption",
    "MentionedChannel",
    "MentionedUser",
    "Message",
    "MessageActivity",
    "MessageCommandInteraction",
    "MessageComponentInteraction",
    "MessageInteraction",
    "Messageable",
    "MethodNotAllowed405",
    "MissingClientSetting",
    "MissingCustomId",
    "Modal",
    "ModalSubmitInteraction",
    "NotFound404",
    "NumberOption",
    "Overwrite",
    "Paginator",
    "PartialEmoji",
    "PartialGuild",
    "PartialUser",
    "Permissions",
    "Presence",
    "Ratelimited429",
    "Reaction",
    "ResolvedDataHandler",
    "Role",
    "RoleOption",
    "RoleTag",
    "Section",
    "SelectMenu",
    "SelectMenuOption",
    "Shard",
    "ShardManager",
    "ShardingRequired",
    "SlashCommand",
    "SlashCommandOptionChoice",
    "SourceChannel",
    "Status",
    "Sticker",
    "StickerItem",
    "StringOption",
    "SubCommandGroup",
    "Subcommand",
    "SystemChannelFlags",
    "Team",
    "TeamMember",
    "TextInput",
    "Thread",
    "ThreadArchived",
    "ThreadMember",
    "TooManyComponents",
    "TooManySelectMenuOptions",
    "TypingContextManager",
    "Unauthorized401",
    "UnavailableGuild",
    "UnhandledEpikCordException",
    "Union",
    "UnknownBucket",
    "User",
    "UserCommandInteraction",
    "UserOption",
    "Utils",
    "VoiceChannel",
    "VoiceOpcode",
    "VoiceRegion",
    "VoiceState",
    "Webhook",
    "WebhookUser",
    "WebsocketClient",
    "WelcomeScreen",
    "WelcomeScreenChannel",
    "cache_manager",
    "channel_manager",
    "close_event_codes",
    "component_from_type",
    "components",
    "decode_rtp_packet",
    "exceptions",
    "generate_rtp_packet",
    "guilds_manager",
    "logger",
    "managers",
    "opcodes",
    "options",
    "partials",
    "roles_manager",
    "rtp_handler",
    "type_enums",
)
