

ActionRow
---------

def add_components(self: Any, components: Any) -> None


def to_dict(self: Any) -> None



Activity
--------

def to_dict(self: Any) -> None
Returns activity class as dict

Returns:
    dict: returns :class:`dict` of :class:`activity`



AllowedMention
--------------


Application
-----------


ApplicationCommand
------------------


ApplicationCommandInteraction
-----------------------------

def create_followup(self: Any, tts: bool, content: Any, embeds: Any, allowed_mentions: Any, components: Any, attachments: Any, suppress_embeds: Any, ephemeral: Any) -> None


def defer(self: Any, show_loading_state: Any) -> None


def delete_followup(self: Any) -> None


def delete_original_response(self: Any) -> None


def edit_followup(self: Any, tts: bool, content: Any, embeds: Any, allowed_mentions: Any, components: Any, attachments: Any, suppress_embeds: Any, ephemeral: Any) -> None


def edit_original_response(self: Any, tts: bool, content: Any, embeds: Any, allowed_mentions: Any, components: Any, attachments: Any, suppress_embeds: Any, ephemeral: Any) -> None


def fetch_original_response(self: Any, skip_cache: Any) -> None


def is_application_command(self: Any) -> None


def is_autocomplete(self: Any) -> None


def is_message_component(self: Any) -> None


def is_modal_submit(self: Any) -> None


def is_ping(self: Any) -> None


def reply(self: Any, tts: bool, content: Any, embeds: Any, allowed_mentions: Any, components: Any, attachments: Any, suppress_embeds: Any, ephemeral: Any) -> None


def send_modal(self: Any, modal: Modal) -> None



ApplicationCommandOption
------------------------


ApplicationCommandPermission
----------------------------

def to_dict(self: Any) -> None



ApplicationCommandSubcommandOption
----------------------------------


Attachment
----------


AttachmentOption
----------------

def to_dict(self: Any) -> None



AutoCompleteInteraction
-----------------------

def create_followup(self: Any, tts: bool, content: Any, embeds: Any, allowed_mentions: Any, components: Any, attachments: Any, suppress_embeds: Any, ephemeral: Any) -> None


def defer(self: Any, show_loading_state: Any) -> None


def delete_followup(self: Any) -> None


def delete_original_response(self: Any) -> None


def edit_followup(self: Any, tts: bool, content: Any, embeds: Any, allowed_mentions: Any, components: Any, attachments: Any, suppress_embeds: Any, ephemeral: Any) -> None


def edit_original_response(self: Any, tts: bool, content: Any, embeds: Any, allowed_mentions: Any, components: Any, attachments: Any, suppress_embeds: Any, ephemeral: Any) -> None


def fetch_original_response(self: Any, skip_cache: Any) -> None


def is_application_command(self: Any) -> None


def is_autocomplete(self: Any) -> None


def is_message_component(self: Any) -> None


def is_modal_submit(self: Any) -> None


def is_ping(self: Any) -> None


def reply(self: Any, choices: Any) -> None


def send_modal(self: Any, modal: Modal) -> None



BadRequest400
-------------


BaseChannel
-----------


BaseComponent
-------------

def set_custom_id(self: Any, custom_id: str) -> None



BaseInteraction
---------------

def create_followup(self: Any, tts: bool, content: Any, embeds: Any, allowed_mentions: Any, components: Any, attachments: Any, suppress_embeds: Any, ephemeral: Any) -> None


def defer(self: Any, show_loading_state: Any) -> None


def delete_followup(self: Any) -> None


def delete_original_response(self: Any) -> None


def edit_followup(self: Any, tts: bool, content: Any, embeds: Any, allowed_mentions: Any, components: Any, attachments: Any, suppress_embeds: Any, ephemeral: Any) -> None


def edit_original_response(self: Any, tts: bool, content: Any, embeds: Any, allowed_mentions: Any, components: Any, attachments: Any, suppress_embeds: Any, ephemeral: Any) -> None


def fetch_original_response(self: Any, skip_cache: Any) -> None


def is_application_command(self: Any) -> None


def is_autocomplete(self: Any) -> None


def is_message_component(self: Any) -> None


def is_modal_submit(self: Any) -> None


def is_ping(self: Any) -> None


def reply(self: Any, tts: bool, content: Any, embeds: Any, allowed_mentions: Any, components: Any, attachments: Any, suppress_embeds: Any, ephemeral: Any) -> None


def send_modal(self: Any, modal: Modal) -> None



BaseSlashCommandOption
----------------------

def to_dict(self: Any) -> None



BooleanOption
-------------

def to_dict(self: Any) -> None



Button
------

def set_custom_id(self: Any, custom_id: str) -> None


def set_emoji(self: Any, emoji: Any) -> None


def set_label(self: Any, label: str) -> None


def set_style(self: Any, style: Any) -> None


def set_url(self: Any, url: str) -> None


def to_dict(self: Any) -> None



CacheManager
------------

def add_to_cache(self: Any, key: Any, value: Any) -> None


def clear_cache(self: Any) -> None


def get_from_cache(self: Any, key: Any) -> None


def is_in_cache(self: Any, key: Any) -> None


def remove_from_cache(self: Any, key: Any) -> None



ChannelCategory
---------------

def create_invite(self: Any, max_age: Any, max_uses: Any, temporary: Any, unique: Any, target_type: Any, target_user_id: Any, target_application_id: Any) -> None


def delete(self: Any, reason: Any) -> None


def delete_overwrite(self: Any, overwrites: Overwrite) -> None


def fetch_invites(self: Any) -> None


def fetch_pinned_messages(self: Any) -> typing.List[EpikCord.Message]



ChannelManager
--------------

def add_to_cache(self: Any, key: Any, value: Any) -> None


def clear_cache(self: Any) -> None


def fetch(self: Any, channel_id: Any, skip_cache: Any) -> None


def format_cache(self: Any) -> None


def get_from_cache(self: Any, key: Any) -> None


def is_in_cache(self: Any, key: Any) -> None


def remove_from_cache(self: Any, key: Any) -> None



ChannelOption
-------------

def to_dict(self: Any) -> None



ChannelOptionChannelTypes
-------------------------


Client
------

def add_section(self: Any, section: Any) -> None


def change_presence(self: Any, presence: Any) -> None


def channel_create(self: Any, data: dict) -> None


def close(self: Any) -> None


def command(self: Any, name: Any, description: Any, guild_ids: Any, options: Any) -> None


def component(self: Any, custom_id: str) -> None
Execute this function when a component with the `custom_id` is interacted with.


def connect(self: Any) -> None


def event(self: Any, func: Any) -> None


def get_event_callback(self: Any, event_name: str, internal: Any) -> None


def guild_create(self: Any, data: Any) -> None


def guild_delete(self: Any, data: dict) -> None


def guild_member_update(self: Any, data: Any) -> None


def guild_members_chunk(self: Any, data: dict) -> None


def handle_close(self: Any) -> None


def handle_event(self: Any, event_name: Any, data: dict) -> None


def handle_events(self: Any) -> None


def heartbeat(self: Any, forced: Any) -> None


def identify(self: Any) -> None


def interaction_create(self: Any, data: Any) -> None


def login(self: Any) -> None


def message_command(self: Any, name: Any) -> None


def message_create(self: Any, data: dict) -> None
Event fired when messages are created


def ready(self: Any, data: dict) -> None


def reconnect(self: Any) -> None


def request_guild_members(self: Any, guild_id: int, query: Any, limit: Any, presences: Any, user_ids: Any, nonce: Any) -> None


def resume(self: Any) -> None


def send_json(self: Any, json: dict) -> None


def unload_section(self: Any, section: Any) -> None


def user_command(self: Any, name: Any) -> None


def voice_server_update(self: Any, data: dict) -> None


def wait_for(self: Any, event_name: str, check: Any, timeout: Any) -> None



ClientApplication
-----------------

def bulk_overwrite_global_application_commands(self: Any, commands: Any) -> None


def bulk_overwrite_guild_application_commands(self: Any, guild_id: str, commands: Any) -> None


def create_global_application_command(self: Any, name: str, description: str, options: Any, default_permission: Any, command_type: Any) -> None


def create_guild_application_command(self: Any, guild_id: str, name: str, description: str, options: Any, default_permission: Any, command_type: Any) -> None


def delete_global_application_command(self: Any, command_id: str) -> None


def delete_guild_application_command(self: Any, guild_id: str, command_id: str) -> None


def edit_application_command_permissions(self: Any, guild_id: str, command_id: Any, permissions: Any) -> None


def edit_global_application_command(self: Any, guild_id: str, command_id: str, name: Any, description: Any, options: Any, default_permissions: Any) -> None


def fetch_application(self: Any) -> None


def fetch_application_command(self: Any, command_id: str) -> None


def fetch_global_application_commands(self: Any) -> typing.List[EpikCord.ApplicationCommand]


def fetch_guild_application_command(self: Any, guild_id: str, command_id: str) -> None


def fetch_guild_application_command_permissions(self: Any, guild_id: str, command_id: str) -> None


def fetch_guild_application_commands(self: Any, guild_id: str) -> None



ClientMessageCommand
--------------------


ClientResponse
--------------

def close(self: Any) -> None


def get_encoding(self: Any) -> <class 'str'>


def json(self: Any, encoding: Any, loads: Any, content_type: Any) -> typing.Any
Read and decodes JSON response.


def raise_for_status(self: Any) -> None


def read(self: Any) -> <class 'bytes'>
Read response payload.


def release(self: Any) -> typing.Any


def start(self: Any, connection: Any) -> ClientResponse
Start response processing.


def text(self: Any, encoding: Any, errors: str) -> <class 'str'>
Read response payload and decode.


def wait_for_close(self: Any) -> None



ClientSession
-------------

def close(self: Any) -> None
Close underlying connector.

Release all acquired resources.


def delete(self: Any, url: Any, kwargs: Any) -> _RequestContextManager
Perform HTTP DELETE request.


def detach(self: Any) -> None
Detach connector from session without closing the former.

Session is switched to closed state anyway.


def get(self: Any, url: Any, allow_redirects: bool, kwargs: Any) -> _RequestContextManager
Perform HTTP GET request.


def head(self: Any, url: Any, allow_redirects: bool, kwargs: Any) -> _RequestContextManager
Perform HTTP HEAD request.


def options(self: Any, url: Any, allow_redirects: bool, kwargs: Any) -> _RequestContextManager
Perform HTTP OPTIONS request.


def patch(self: Any, url: Any, data: Any, kwargs: Any) -> _RequestContextManager
Perform HTTP PATCH request.


def post(self: Any, url: Any, data: Any, kwargs: Any) -> _RequestContextManager
Perform HTTP POST request.


def put(self: Any, url: Any, data: Any, kwargs: Any) -> _RequestContextManager
Perform HTTP PUT request.


def request(self: Any, method: str, url: Any, kwargs: Any) -> _RequestContextManager
Perform HTTP request.


def ws_connect(self: Any, url: Any, method: str, protocols: Any, timeout: float, receive_timeout: Any, autoclose: bool, autoping: bool, heartbeat: Any, auth: Any, origin: Any, params: Any, headers: Any, proxy: Any, proxy_auth: Any, ssl: Any, verify_ssl: Any, fingerprint: Any, ssl_context: Any, proxy_headers: Any, compress: int, max_msg_size: int) -> _WSRequestContextManager
Initiate websocket connection.



ClientSlashCommand
------------------

def option_autocomplete(self: Any, option_name: str) -> None



ClientUser
----------

def edit(self: Any, username: Any, avatar: Any) -> None


def fetch(self: Any) -> None



ClientUserCommand
-----------------


ClosedWebSocketConnection
-------------------------


Colour
------

def to_rgb(self: Any) -> typing.Tuple[int, int, int]
Returns an rgb color as a tuple



Colour
------

def to_rgb(self: Any) -> typing.Tuple[int, int, int]
Returns an rgb color as a tuple



CommandsSection
---------------


CustomIdIsTooBig
----------------


DMChannel
---------


DisallowedIntents
-----------------


DiscordAPIError
---------------


Embed
-----

def add_field(self: Any, name: str, value: str, inline: bool) -> None


def set_author(self: Any, name: Any, url: Any, icon_url: Any, proxy_icon_url: Any) -> None


def set_color(self: Any, colour: Colour) -> None


def set_description(self: Any, description: Any) -> None


def set_fields(self: Any, fields: Any) -> None


def set_footer(self: Any, text: Any, icon_url: Any, proxy_icon_url: Any) -> None


def set_image(self: Any, url: Any, proxy_url: Any, height: Any, width: Any) -> None


def set_provider(self: Any, name: Any, url: Any) -> None


def set_thumbnail(self: Any, url: Any, proxy_url: Any, height: Any, width: Any) -> None


def set_timestamp(self: Any, timestamp: datetime) -> None


def set_title(self: Any, title: Any) -> None


def set_url(self: Any, url: Any) -> None


def set_video(self: Any, url: Any, proxy_url: Any, height: Any, width: Any) -> None


def to_dict(self: Any) -> None



Emoji
-----

def delete(self: Any, reason: Any) -> None


def edit(self: Any, name: Any, roles: Any, reason: Any) -> None



EpikCordException
-----------------


EventHandler
------------

def channel_create(self: Any, data: dict) -> None


def component(self: Any, custom_id: str) -> None
Execute this function when a component with the `custom_id` is interacted with.


def event(self: Any, func: Any) -> None


def get_event_callback(self: Any, event_name: str, internal: Any) -> None


def guild_create(self: Any, data: Any) -> None


def guild_delete(self: Any, data: dict) -> None


def guild_member_update(self: Any, data: Any) -> None


def guild_members_chunk(self: Any, data: dict) -> None


def handle_event(self: Any, event_name: Any, data: dict) -> None


def handle_events(self: Any) -> None


def interaction_create(self: Any, data: Any) -> None


def message_create(self: Any, data: dict) -> None
Event fired when messages are created


def ready(self: Any, data: dict) -> None


def voice_server_update(self: Any, data: dict) -> None


def wait_for(self: Any, event_name: str, check: Any, timeout: Any) -> None



EventsSection
-------------


FailedToConnectToVoice
----------------------


File
----


Flag
----

def calculate_from_turned(self: Any) -> None



Forbidden403
------------


GateawayUnavailable502
----------------------


Guild
-----

def create_channel(self: Any, name: str, reason: Any, type: Any, topic: Any, bitrate: Any, user_limit: Any, rate_limit_per_user: Any, position: Any, permission_overwrites: Any, parent_id: Any, nsfw: Any) -> None
Creates a channel.

Parameters
----------
name: str
    The name of the channel.
reason: Optional[str]
    The reason for creating the channel.
type: Optional[int]
    The type of the channel.
topic: Optional[str]
    The topic of the channel.
bitrate: Optional[int]
    The bitrate of the channel.
user_limit: Optional[int]
    The user limit of the channel.
rate_limit_per_user: Optional[int]
    The rate limit per user of the channel.
position: Optional[int]
    The position of the channel.
permission_overwrites: List[Optional[Overwrite]]
    The permission overwrites of the channel.
parent_id: Optional[str]
    The parent id of the channel.
nsfw: Optional[bool]
    Whether the channel is nsfw.


def delete(self: Any) -> None


def edit(self: Any, name: Any, verification_level: Any, default_message_notifications: Any, explicit_content_filter: Any, afk_channel_id: Any, afk_timeout: Any, owner_id: Any, system_channel_id: Any, system_channel_flags: Any, rules_channel_id: Any, preferred_locale: Any, features: Any, description: Any, premium_progress_bar_enabled: Any, reason: Any) -> None
Edits the guild.

Parameters
----------
name: Optional[str]
    The name of the guild.
verification_level: Optional[int]
    The verification level of the guild.
default_message_notifications: Optional[int]
    The default message notifications of the guild.
explicit_content_filter: Optional[int]
    The explicit content filter of the guild.
afk_channel_id: Optional[str]
    The afk channel id of the guild.
afk_timeout: Optional[int]
    The afk timeout of the guild.
owner_id: Optional[str]
    The owner id of the guild.
system_channel_id: Optional[str]
    The system channel id of the guild.
system_channel_flags: Optional[SystemChannelFlags]
    The system channel flags of the guild.
rules_channel_id: Optional[str]
    The rules channel id of the guild.
preferred_locale: Optional[str]
    The preferred locale of the guild.
features: Optional[List[str]]
    The features of the guild.
description: Optional[str]
    The description of the guild.
premium_progress_bar_enabled: Optional[bool]
    Whether the guild has the premium progress bar enabled.

Returns
-------
:class:`EpikCord.Guild`


def fetch_channels(self: Any) -> typing.List[EpikCord.GuildChannel]
Fetches the guild channels.

Returns
-------
List[GuildChannel]
    The guild channels.


def fetch_guild_preview(self: Any) -> <class 'EpikCord.GuildPreview'>
Fetches the guild preview.

Returns
-------
GuildPreview
    The guild preview.



GuildApplicationCommandPermission
---------------------------------

def to_dict(self: Any) -> None



GuildBan
--------


GuildChannel
------------

def create_invite(self: Any, max_age: Any, max_uses: Any, temporary: Any, unique: Any, target_type: Any, target_user_id: Any, target_application_id: Any) -> None


def delete(self: Any, reason: Any) -> None


def delete_overwrite(self: Any, overwrites: Overwrite) -> None


def fetch_invites(self: Any) -> None


def fetch_pinned_messages(self: Any) -> typing.List[EpikCord.Message]



GuildManager
------------

def add_to_cache(self: Any, key: Any, value: Any) -> None


def clear_cache(self: Any) -> None


def fetch(self: Any, guild_id: str, skip_cache: Any, with_counts: Any) -> None


def format_cache(self: Any) -> None


def get_from_cache(self: Any, key: Any) -> None


def is_in_cache(self: Any, key: Any) -> None


def remove_from_cache(self: Any, key: Any) -> None



GuildMember
-----------

def fetch_message(self: Any, message_id: str) -> <class 'EpikCord.Message'>


def fetch_messages(self: Any, around: Any, before: Any, after: Any, limit: Any) -> typing.List[EpikCord.Message]


def send(self: Any, content: Any, embeds: Any, components: Any, tts: Any, allowed_mentions: Any, sticker_ids: Any, attachments: Any, suppress_embeds: bool) -> <class 'EpikCord.Message'>



GuildNewsChannel
----------------

def bulk_delete(self: Any, message_ids: Any, reason: Any) -> None


def create_invite(self: Any, max_age: Any, max_uses: Any, temporary: Any, unique: Any, target_type: Any, target_user_id: Any, target_application_id: Any) -> None


def create_webhook(self: Any, name: str, avatar: Any, reason: Any) -> None


def delete(self: Any, reason: Any) -> None


def delete_overwrite(self: Any, overwrites: Overwrite) -> None


def fetch_invites(self: Any) -> None


def fetch_message(self: Any, message_id: str) -> <class 'EpikCord.Message'>


def fetch_messages(self: Any, around: Any, before: Any, after: Any, limit: Any) -> typing.List[EpikCord.Message]


def fetch_pinned_messages(self: Any) -> typing.List[EpikCord.Message]


def follow(self: Any, webhook_channel_id: str) -> None


def list_joined_private_archived_threads(self: Any, before: Any, limit: Any) -> typing.Dict[str, typing.Union[typing.List[EpikCord.Messageable], typing.List[EpikCord.ThreadMember], bool]]


def list_private_archived_threads(self: Any, before: Any, limit: Any) -> typing.Dict[str, typing.Union[typing.List[EpikCord.Messageable], typing.List[EpikCord.ThreadMember], bool]]


def list_public_archived_threads(self: Any, before: Any, limit: Any) -> typing.Dict[str, typing.Union[typing.List[EpikCord.Messageable], typing.List[EpikCord.ThreadMember], bool]]


def send(self: Any, content: Any, embeds: Any, components: Any, tts: Any, allowed_mentions: Any, sticker_ids: Any, attachments: Any, suppress_embeds: bool) -> <class 'EpikCord.Message'>


def start_thread(self: Any, name: str, auto_archive_duration: Any, type: Any, invitable: Any, rate_limit_per_user: Any, reason: Any) -> None



GuildNewsThread
---------------

def add_member(self: Any, member_id: str) -> None


def bulk_delete(self: Any, message_ids: Any, reason: Any) -> None


def create_invite(self: Any, max_age: Any, max_uses: Any, temporary: Any, unique: Any, target_type: Any, target_user_id: Any, target_application_id: Any) -> None


def create_webhook(self: Any, name: str, avatar: Any, reason: Any) -> None


def delete(self: Any, reason: Any) -> None


def delete_overwrite(self: Any, overwrites: Overwrite) -> None


def fetch_invites(self: Any) -> None


def fetch_member(self: Any, member_id: str) -> <class 'EpikCord.ThreadMember'>


def fetch_message(self: Any, message_id: str) -> <class 'EpikCord.Message'>


def fetch_messages(self: Any, around: Any, before: Any, after: Any, limit: Any) -> typing.List[EpikCord.Message]


def fetch_pinned_messages(self: Any) -> typing.List[EpikCord.Message]


def follow(self: Any, webhook_channel_id: str) -> None


def join(self: Any) -> None


def leave(self: Any) -> None


def list_joined_private_archived_threads(self: Any, before: Any, limit: Any) -> typing.Dict[str, typing.Union[typing.List[EpikCord.Messageable], typing.List[EpikCord.ThreadMember], bool]]


def list_members(self: Any) -> typing.List[EpikCord.ThreadMember]


def list_private_archived_threads(self: Any, before: Any, limit: Any) -> typing.Dict[str, typing.Union[typing.List[EpikCord.Messageable], typing.List[EpikCord.ThreadMember], bool]]


def list_public_archived_threads(self: Any, before: Any, limit: Any) -> typing.Dict[str, typing.Union[typing.List[EpikCord.Messageable], typing.List[EpikCord.ThreadMember], bool]]


def remove_member(self: Any, member_id: str) -> None


def send(self: Any, content: Any, embeds: Any, components: Any, tts: Any, allowed_mentions: Any, sticker_ids: Any, attachments: Any, suppress_embeds: bool) -> <class 'EpikCord.Message'>


def start_thread(self: Any, name: str, auto_archive_duration: Any, type: Any, invitable: Any, rate_limit_per_user: Any, reason: Any) -> None



GuildPreview
------------


GuildScheduledEvent
-------------------


GuildStageChannel
-----------------


GuildTextChannel
----------------

def bulk_delete(self: Any, message_ids: Any, reason: Any) -> None


def create_invite(self: Any, max_age: Any, max_uses: Any, temporary: Any, unique: Any, target_type: Any, target_user_id: Any, target_application_id: Any) -> None


def create_webhook(self: Any, name: str, avatar: Any, reason: Any) -> None


def delete(self: Any, reason: Any) -> None


def delete_overwrite(self: Any, overwrites: Overwrite) -> None


def fetch_invites(self: Any) -> None


def fetch_message(self: Any, message_id: str) -> <class 'EpikCord.Message'>


def fetch_messages(self: Any, around: Any, before: Any, after: Any, limit: Any) -> typing.List[EpikCord.Message]


def fetch_pinned_messages(self: Any) -> typing.List[EpikCord.Message]


def list_joined_private_archived_threads(self: Any, before: Any, limit: Any) -> typing.Dict[str, typing.Union[typing.List[EpikCord.Messageable], typing.List[EpikCord.ThreadMember], bool]]


def list_private_archived_threads(self: Any, before: Any, limit: Any) -> typing.Dict[str, typing.Union[typing.List[EpikCord.Messageable], typing.List[EpikCord.ThreadMember], bool]]


def list_public_archived_threads(self: Any, before: Any, limit: Any) -> typing.Dict[str, typing.Union[typing.List[EpikCord.Messageable], typing.List[EpikCord.ThreadMember], bool]]


def send(self: Any, content: Any, embeds: Any, components: Any, tts: Any, allowed_mentions: Any, sticker_ids: Any, attachments: Any, suppress_embeds: bool) -> <class 'EpikCord.Message'>


def start_thread(self: Any, name: str, auto_archive_duration: Any, type: Any, invitable: Any, rate_limit_per_user: Any, reason: Any) -> None



GuildWidget
-----------


GuildWidgetSettings
-------------------


HTTPClient
----------

def close(self: Any) -> None
Close underlying connector.

Release all acquired resources.


def delete(self: Any, url: Any, args: Any, to_discord: bool, kwargs: Any) -> None
Perform HTTP DELETE request.


def detach(self: Any) -> None
Detach connector from session without closing the former.

Session is switched to closed state anyway.


def get(self: Any, url: Any, args: Any, to_discord: bool, kwargs: Any) -> None
Perform HTTP GET request.


def head(self: Any, url: Any, args: Any, to_discord: bool, kwargs: Any) -> None
Perform HTTP HEAD request.


def log_request(self: Any, res: Any) -> None


def options(self: Any, url: Any, allow_redirects: bool, kwargs: Any) -> _RequestContextManager
Perform HTTP OPTIONS request.


def patch(self: Any, url: Any, args: Any, to_discord: bool, kwargs: Any) -> None
Perform HTTP PATCH request.


def post(self: Any, url: Any, args: Any, to_discord: bool, kwargs: Any) -> None
Perform HTTP POST request.


def put(self: Any, url: Any, args: Any, to_discord: bool, kwargs: Any) -> None
Perform HTTP PUT request.


def request(self: Any, method: str, url: Any, kwargs: Any) -> _RequestContextManager
Perform HTTP request.


def ws_connect(self: Any, url: Any, method: str, protocols: Any, timeout: float, receive_timeout: Any, autoclose: bool, autoping: bool, heartbeat: Any, auth: Any, origin: Any, params: Any, headers: Any, proxy: Any, proxy_auth: Any, ssl: Any, verify_ssl: Any, fingerprint: Any, ssl_context: Any, proxy_headers: Any, compress: int, max_msg_size: int) -> _WSRequestContextManager
Initiate websocket connection.



IntegerOption
-------------

def to_dict(self: Any) -> None



Integration
-----------


IntegrationAccount
------------------


Intents
-------

def calculate_from_turned(self: Any) -> None



InternalServerError5xx
----------------------


InvalidApplicationCommandOptionType
-----------------------------------


InvalidApplicationCommandType
-----------------------------


InvalidArgumentType
-------------------


InvalidComponentStyle
---------------------


InvalidData
-----------


InvalidIntents
--------------


InvalidOption
-------------


InvalidStatus
-------------


InvalidToken
------------


Invite
------


LabelIsTooBig
-------------


MentionableOption
-----------------

def to_dict(self: Any) -> None



MentionedChannel
----------------


MentionedUser
-------------

def fetch_message(self: Any, message_id: str) -> <class 'EpikCord.Message'>


def fetch_messages(self: Any, around: Any, before: Any, after: Any, limit: Any) -> typing.List[EpikCord.Message]


def send(self: Any, content: Any, embeds: Any, components: Any, tts: Any, allowed_mentions: Any, sticker_ids: Any, attachments: Any, suppress_embeds: bool) -> <class 'EpikCord.Message'>



Message
-------

def add_reaction(self: Any, emoji: str) -> None


def crosspost(self: Any) -> None


def delete(self: Any) -> None


def delete_all_reactions(self: Any) -> None


def delete_reaction_for_emoji(self: Any, emoji: str) -> None


def edit(self: Any, message_data: dict) -> None


def fetch_reactions(self: Any, after: Any, limit: Any) -> typing.List[EpikCord.Reaction]


def pin(self: Any, reason: Any) -> None


def remove_reaction(self: Any, emoji: str, user: Any) -> None


def start_thread(self: Any, name: str, auto_archive_duration: Any, rate_limit_per_user: Any) -> None


def unpin(self: Any, reason: Any) -> None



MessageActivity
---------------


MessageCommandInteraction
-------------------------

def create_followup(self: Any, tts: bool, content: Any, embeds: Any, allowed_mentions: Any, components: Any, attachments: Any, suppress_embeds: Any, ephemeral: Any) -> None


def defer(self: Any, show_loading_state: Any) -> None


def delete_followup(self: Any) -> None


def delete_original_response(self: Any) -> None


def edit_followup(self: Any, tts: bool, content: Any, embeds: Any, allowed_mentions: Any, components: Any, attachments: Any, suppress_embeds: Any, ephemeral: Any) -> None


def edit_original_response(self: Any, tts: bool, content: Any, embeds: Any, allowed_mentions: Any, components: Any, attachments: Any, suppress_embeds: Any, ephemeral: Any) -> None


def fetch_original_response(self: Any, skip_cache: Any) -> None


def is_application_command(self: Any) -> None


def is_autocomplete(self: Any) -> None


def is_message_component(self: Any) -> None


def is_modal_submit(self: Any) -> None


def is_ping(self: Any) -> None


def reply(self: Any, tts: bool, content: Any, embeds: Any, allowed_mentions: Any, components: Any, attachments: Any, suppress_embeds: Any, ephemeral: Any) -> None


def send_modal(self: Any, modal: Modal) -> None



MessageComponentInteraction
---------------------------

def create_followup(self: Any, tts: bool, content: Any, embeds: Any, allowed_mentions: Any, components: Any, attachments: Any, suppress_embeds: Any, ephemeral: Any) -> None


def defer(self: Any, show_loading_state: Any) -> None


def defer_update(self: Any) -> None


def delete_followup(self: Any) -> None


def delete_original_response(self: Any) -> None


def edit_followup(self: Any, tts: bool, content: Any, embeds: Any, allowed_mentions: Any, components: Any, attachments: Any, suppress_embeds: Any, ephemeral: Any) -> None


def edit_original_response(self: Any, tts: bool, content: Any, embeds: Any, allowed_mentions: Any, components: Any, attachments: Any, suppress_embeds: Any, ephemeral: Any) -> None


def fetch_original_response(self: Any, skip_cache: Any) -> None


def is_action_row(self: Any) -> None


def is_application_command(self: Any) -> None


def is_autocomplete(self: Any) -> None


def is_button(self: Any) -> None


def is_message_component(self: Any) -> None


def is_modal_submit(self: Any) -> None


def is_ping(self: Any) -> None


def is_select_menu(self: Any) -> None


def is_text_input(self: Any) -> None


def reply(self: Any, tts: bool, content: Any, embeds: Any, allowed_mentions: Any, components: Any, attachments: Any, suppress_embeds: Any, ephemeral: Any) -> None


def send_modal(self: Any, modal: Modal) -> None


def update(self: Any, tts: bool, content: Any, embeds: Any, allowed_mentions: Any, components: Any, attachments: Any, suppress_embeds: Any) -> None



MessageInteraction
------------------


Messageable
-----------

def fetch_message(self: Any, message_id: str) -> <class 'EpikCord.Message'>


def fetch_messages(self: Any, around: Any, before: Any, after: Any, limit: Any) -> typing.List[EpikCord.Message]


def send(self: Any, content: Any, embeds: Any, components: Any, tts: Any, allowed_mentions: Any, sticker_ids: Any, attachments: Any, suppress_embeds: bool) -> <class 'EpikCord.Message'>



MethodNotAllowed405
-------------------


MissingClientSetting
--------------------


MissingCustomId
---------------


Modal
-----

def to_dict(self: Any) -> None



ModalSubmitInteraction
----------------------

def create_followup(self: Any, tts: bool, content: Any, embeds: Any, allowed_mentions: Any, components: Any, attachments: Any, suppress_embeds: Any, ephemeral: Any) -> None


def defer(self: Any, show_loading_state: Any) -> None


def delete_followup(self: Any) -> None


def delete_original_response(self: Any) -> None


def edit_followup(self: Any, tts: bool, content: Any, embeds: Any, allowed_mentions: Any, components: Any, attachments: Any, suppress_embeds: Any, ephemeral: Any) -> None


def edit_original_response(self: Any, tts: bool, content: Any, embeds: Any, allowed_mentions: Any, components: Any, attachments: Any, suppress_embeds: Any, ephemeral: Any) -> None


def fetch_original_response(self: Any, skip_cache: Any) -> None


def is_application_command(self: Any) -> None


def is_autocomplete(self: Any) -> None


def is_message_component(self: Any) -> None


def is_modal_submit(self: Any) -> None


def is_ping(self: Any) -> None


def reply(self: Any, tts: bool, content: Any, embeds: Any, allowed_mentions: Any, components: Any, attachments: Any, suppress_embeds: Any, ephemeral: Any) -> None


def send_modal(self: Any, args: Any, kwargs: Any) -> None



NotFound404
-----------


NumberOption
------------

def to_dict(self: Any) -> None



Overwrite
---------


Paginator
---------

def add_page(self: Any, page: Embed) -> None


def back(self: Any) -> None


def current(self: Any) -> <class 'EpikCord.Embed'>


def forward(self: Any) -> None


def remove_page(self: Any, page: Embed) -> None



PartialEmoji
------------

def to_dict(self: Any) -> None



PartialGuild
------------


PartialUser
-----------


Permissions
-----------

def calculate_from_turned(self: Any) -> None



Presence
--------

def to_dict(self: Any) -> None



PrivateThread
-------------

def add_member(self: Any, member_id: str) -> None


def bulk_delete(self: Any, message_ids: Any, reason: Any) -> None


def fetch_member(self: Any, member_id: str) -> <class 'EpikCord.ThreadMember'>


def join(self: Any) -> None


def leave(self: Any) -> None


def list_members(self: Any) -> typing.List[EpikCord.ThreadMember]


def remove_member(self: Any, member_id: str) -> None



RatelimitHandler
----------------

def is_ratelimited(self: Any) -> <class 'bool'>
Checks if the client is ratelimited.


def process_headers(self: Any, headers: dict) -> None
Read the headers from a request and then digest it.



Ratelimited429
--------------


Reaction
--------


ResolvedDataHandler
-------------------


Role
----


RoleOption
----------

def to_dict(self: Any) -> None



RoleTag
-------


SelectMenu
----------

def add_options(self: Any, options: Any) -> None


def set_custom_id(self: Any, custom_id: str) -> None


def set_disabled(self: Any, disabled: bool) -> None


def set_max_values(self: Any, max: int) -> None


def set_min_values(self: Any, min: int) -> None


def set_placeholder(self: Any, placeholder: str) -> None


def to_dict(self: Any) -> None



SelectMenuOption
----------------

def to_dict(self: Any) -> None



Shard
-----

def change_presence(self: Any, presence: Any) -> None


def channel_create(self: Any, data: dict) -> None


def close(self: Any) -> None


def component(self: Any, custom_id: str) -> None
Execute this function when a component with the `custom_id` is interacted with.


def connect(self: Any) -> None


def event(self: Any, func: Any) -> None


def get_event_callback(self: Any, event_name: str, internal: Any) -> None


def guild_create(self: Any, data: Any) -> None


def guild_delete(self: Any, data: dict) -> None


def guild_member_update(self: Any, data: Any) -> None


def guild_members_chunk(self: Any, data: dict) -> None


def handle_close(self: Any) -> None


def handle_event(self: Any, event_name: Any, data: dict) -> None


def handle_events(self: Any) -> None


def heartbeat(self: Any, forced: Any) -> None


def identify(self: Any) -> None


def interaction_create(self: Any, data: Any) -> None


def login(self: Any) -> None


def message_create(self: Any, data: dict) -> None
Event fired when messages are created


def ready(self: Any, data: dict) -> None


def reconnect(self: Any) -> None


def request_guild_members(self: Any, guild_id: int, query: Any, limit: Any, presences: Any, user_ids: Any, nonce: Any) -> None


def resume(self: Any) -> None


def send_json(self: Any, json: dict) -> None


def voice_server_update(self: Any, data: dict) -> None


def wait_for(self: Any, event_name: str, check: Any, timeout: Any) -> None



ShardingRequired
----------------


SlashCommand
------------

def to_dict(self: Any) -> None



SlashCommandOptionChoice
------------------------

def to_dict(self: Any) -> None



SourceChannel
-------------


Status
------


Sticker
-------


StickerItem
-----------


StringOption
------------

def to_dict(self: Any) -> None



SubCommandGroup
---------------

def to_dict(self: Any) -> None



Subcommand
----------

def to_dict(self: Any) -> None



SystemChannelFlags
------------------


Team
----


TeamMember
----------


TextInput
---------

def set_custom_id(self: Any, custom_id: str) -> None


def to_dict(self: Any) -> None



Thread
------

def add_member(self: Any, member_id: str) -> None


def bulk_delete(self: Any, message_ids: Any, reason: Any) -> None


def fetch_member(self: Any, member_id: str) -> <class 'EpikCord.ThreadMember'>


def join(self: Any) -> None


def leave(self: Any) -> None


def list_members(self: Any) -> typing.List[EpikCord.ThreadMember]


def remove_member(self: Any, member_id: str) -> None



ThreadArchived
--------------


ThreadMember
------------


TooManyComponents
-----------------


TooManySelectMenuOptions
------------------------


TypeVar
-------


Unauthorized401
---------------


UnavailableGuild
----------------


UnhandledEpikCordException
--------------------------


User
----

def fetch_message(self: Any, message_id: str) -> <class 'EpikCord.Message'>


def fetch_messages(self: Any, around: Any, before: Any, after: Any, limit: Any) -> typing.List[EpikCord.Message]


def send(self: Any, content: Any, embeds: Any, components: Any, tts: Any, allowed_mentions: Any, sticker_ids: Any, attachments: Any, suppress_embeds: bool) -> <class 'EpikCord.Message'>



UserCommandInteraction
----------------------

def create_followup(self: Any, tts: bool, content: Any, embeds: Any, allowed_mentions: Any, components: Any, attachments: Any, suppress_embeds: Any, ephemeral: Any) -> None


def defer(self: Any, show_loading_state: Any) -> None


def delete_followup(self: Any) -> None


def delete_original_response(self: Any) -> None


def edit_followup(self: Any, tts: bool, content: Any, embeds: Any, allowed_mentions: Any, components: Any, attachments: Any, suppress_embeds: Any, ephemeral: Any) -> None


def edit_original_response(self: Any, tts: bool, content: Any, embeds: Any, allowed_mentions: Any, components: Any, attachments: Any, suppress_embeds: Any, ephemeral: Any) -> None


def fetch_original_response(self: Any, skip_cache: Any) -> None


def is_application_command(self: Any) -> None


def is_autocomplete(self: Any) -> None


def is_message_component(self: Any) -> None


def is_modal_submit(self: Any) -> None


def is_ping(self: Any) -> None


def reply(self: Any, tts: bool, content: Any, embeds: Any, allowed_mentions: Any, components: Any, attachments: Any, suppress_embeds: Any, ephemeral: Any) -> None


def send_modal(self: Any, modal: Modal) -> None



UserOption
----------

def to_dict(self: Any) -> None



Utils
-----

def cancel_tasks(self: Any, loop: Any) -> None


def channel_from_type(self: Any, channel_data: dict) -> None


def cleanup_loop(self: Any, loop: Any) -> None


def component_from_type(self: Any, component_data: dict) -> None


def compute_timedelta(self: Any, dt: datetime) -> None


def escape_markdown(self: Any, text: str, as_needed: bool, ignore_links: bool) -> <class 'str'>


def escape_mentions(self: Any, text: str) -> <class 'str'>


def get_mime_type_for_image(self: Any, data: bytes) -> None


def interaction_from_type(self: Any, data: Any) -> None


def remove_markdown(self: Any, text: str, ignore_links: bool) -> <class 'str'>


def sleep_until(self: Any, when: Any, result: Any) -> typing.Optional[~T]


def utcnow(self: Any) -> <class 'datetime.datetime'>



VoiceChannel
------------

def create_invite(self: Any, max_age: Any, max_uses: Any, temporary: Any, unique: Any, target_type: Any, target_user_id: Any, target_application_id: Any) -> None


def delete(self: Any, reason: Any) -> None


def delete_overwrite(self: Any, overwrites: Overwrite) -> None


def fetch_invites(self: Any) -> None


def fetch_pinned_messages(self: Any) -> typing.List[EpikCord.Message]



VoiceState
----------


VoiceWebsocketClient
--------------------

def connect(self: Any, muted: Any, deafened: Any) -> None



Webhook
-------


WebhookUser
-----------


WebsocketClient
---------------

def change_presence(self: Any, presence: Any) -> None


def channel_create(self: Any, data: dict) -> None


def close(self: Any) -> None


def component(self: Any, custom_id: str) -> None
Execute this function when a component with the `custom_id` is interacted with.


def connect(self: Any) -> None


def event(self: Any, func: Any) -> None


def get_event_callback(self: Any, event_name: str, internal: Any) -> None


def guild_create(self: Any, data: Any) -> None


def guild_delete(self: Any, data: dict) -> None


def guild_member_update(self: Any, data: Any) -> None


def guild_members_chunk(self: Any, data: dict) -> None


def handle_close(self: Any) -> None


def handle_event(self: Any, event_name: Any, data: dict) -> None


def handle_events(self: Any) -> None


def heartbeat(self: Any, forced: Any) -> None


def identify(self: Any) -> None


def interaction_create(self: Any, data: Any) -> None


def login(self: Any) -> None


def message_create(self: Any, data: dict) -> None
Event fired when messages are created


def ready(self: Any, data: dict) -> None


def reconnect(self: Any) -> None


def request_guild_members(self: Any, guild_id: int, query: Any, limit: Any, presences: Any, user_ids: Any, nonce: Any) -> None


def resume(self: Any) -> None


def send_json(self: Any, json: dict) -> None


def voice_server_update(self: Any, data: dict) -> None


def wait_for(self: Any, event_name: str, check: Any, timeout: Any) -> None



WelcomeScreen
-------------


WelcomeScreenChannel
--------------------
