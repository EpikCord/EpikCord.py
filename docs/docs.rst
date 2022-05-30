

ActionRow
---------

def add_components(, components: Any) -> None


def to_dict() -> None



Activity
--------

def to_dict() -> None
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

def create_followup(, tts: bool, content: Any, embeds: Any, allowed_mentions: Any, components: Any, attachments: Any, suppress_embeds: Any, ephemeral: Any) -> None


def defer(, show_loading_state: Any) -> None


def delete_followup() -> None


def delete_original_response() -> None


def edit_followup(, tts: bool, content: Any, embeds: Any, allowed_mentions: Any, components: Any, attachments: Any, suppress_embeds: Any, ephemeral: Any) -> None


def edit_original_response(, tts: bool, content: Any, embeds: Any, allowed_mentions: Any, components: Any, attachments: Any, suppress_embeds: Any, ephemeral: Any) -> None


def fetch_original_response(, skip_cache: Any) -> None


def is_application_command() -> None


def is_autocomplete() -> None


def is_message_component() -> None


def is_modal_submit() -> None


def is_ping() -> None


def reply(, tts: bool, content: Any, embeds: Any, allowed_mentions: Any, components: Any, attachments: Any, suppress_embeds: Any, ephemeral: Any) -> None


def send_modal(, modal: Modal) -> None



ApplicationCommandOption
------------------------


ApplicationCommandPermission
----------------------------

def to_dict() -> None



ApplicationCommandSubcommandOption
----------------------------------


Attachment
----------


AttachmentOption
----------------

def to_dict() -> None



AutoCompleteInteraction
-----------------------

def create_followup(, tts: bool, content: Any, embeds: Any, allowed_mentions: Any, components: Any, attachments: Any, suppress_embeds: Any, ephemeral: Any) -> None


def defer(, show_loading_state: Any) -> None


def delete_followup() -> None


def delete_original_response() -> None


def edit_followup(, tts: bool, content: Any, embeds: Any, allowed_mentions: Any, components: Any, attachments: Any, suppress_embeds: Any, ephemeral: Any) -> None


def edit_original_response(, tts: bool, content: Any, embeds: Any, allowed_mentions: Any, components: Any, attachments: Any, suppress_embeds: Any, ephemeral: Any) -> None


def fetch_original_response(, skip_cache: Any) -> None


def is_application_command() -> None


def is_autocomplete() -> None


def is_message_component() -> None


def is_modal_submit() -> None


def is_ping() -> None


def reply(, choices: Any) -> None


def send_modal(, modal: Modal) -> None



BadRequest400
-------------


BaseChannel
-----------


BaseComponent
-------------

def set_custom_id(, custom_id: str) -> None



BaseInteraction
---------------

def create_followup(, tts: bool, content: Any, embeds: Any, allowed_mentions: Any, components: Any, attachments: Any, suppress_embeds: Any, ephemeral: Any) -> None


def defer(, show_loading_state: Any) -> None


def delete_followup() -> None


def delete_original_response() -> None


def edit_followup(, tts: bool, content: Any, embeds: Any, allowed_mentions: Any, components: Any, attachments: Any, suppress_embeds: Any, ephemeral: Any) -> None


def edit_original_response(, tts: bool, content: Any, embeds: Any, allowed_mentions: Any, components: Any, attachments: Any, suppress_embeds: Any, ephemeral: Any) -> None


def fetch_original_response(, skip_cache: Any) -> None


def is_application_command() -> None


def is_autocomplete() -> None


def is_message_component() -> None


def is_modal_submit() -> None


def is_ping() -> None


def reply(, tts: bool, content: Any, embeds: Any, allowed_mentions: Any, components: Any, attachments: Any, suppress_embeds: Any, ephemeral: Any) -> None


def send_modal(, modal: Modal) -> None



BaseSlashCommandOption
----------------------

def to_dict() -> None



BooleanOption
-------------

def to_dict() -> None



Button
------

def set_custom_id(, custom_id: str) -> None


def set_emoji(, emoji: Any) -> None


def set_label(, label: str) -> None


def set_style(, style: Any) -> None


def set_url(, url: str) -> None


def to_dict() -> None



CacheManager
------------

def add_to_cache(, key: Any, value: Any) -> None


def clear_cache() -> None


def get_from_cache(, key: Any) -> None


def is_in_cache(, key: Any) -> None


def remove_from_cache(, key: Any) -> None



ChannelCategory
---------------

def create_invite(, max_age: Any, max_uses: Any, temporary: Any, unique: Any, target_type: Any, target_user_id: Any, target_application_id: Any) -> None


def delete(, reason: Any) -> None


def delete_overwrite(, overwrites: Overwrite) -> None


def fetch_invites() -> None


def fetch_pinned_messages() -> typing.List[EpikCord.Message]



ChannelManager
--------------

def add_to_cache(, key: Any, value: Any) -> None


def clear_cache() -> None


def fetch(, channel_id: Any, skip_cache: Any) -> None


def format_cache() -> None


def get_from_cache(, key: Any) -> None


def is_in_cache(, key: Any) -> None


def remove_from_cache(, key: Any) -> None



ChannelOption
-------------

def to_dict() -> None



ChannelOptionChannelTypes
-------------------------


Client
------

def add_section(, section: Any) -> None


def change_presence(, presence: Any) -> None


def channel_create(, data: dict) -> None


def close() -> None


def command(, name: Any, description: Any, guild_ids: Any, options: Any) -> None


def component(, custom_id: str) -> None
Execute this function when a component with the `custom_id` is interacted with.


def connect() -> None


def event(, func: Any) -> None


def get_event_callback(, event_name: str, internal: Any) -> None


def guild_create(, data: Any) -> None


def guild_delete(, data: dict) -> None


def guild_member_update(, data: Any) -> None


def guild_members_chunk(, data: dict) -> None


def handle_close() -> None


def handle_event(, event_name: Any, data: dict) -> None


def handle_events() -> None


def heartbeat(, forced: Any) -> None


def identify() -> None


def interaction_create(, data: Any) -> None


def login() -> None


def message_command(, name: Any) -> None


def message_create(, data: dict) -> None
Event fired when messages are created


def ready(, data: dict) -> None


def reconnect() -> None


def request_guild_members(, guild_id: int, query: Any, limit: Any, presences: Any, user_ids: Any, nonce: Any) -> None


def resume() -> None


def send_json(, json: dict) -> None


def unload_section(, section: Any) -> None


def user_command(, name: Any) -> None


def voice_server_update(, data: dict) -> None


def wait_for(, event_name: str, check: Any, timeout: Any) -> None



ClientApplication
-----------------

def bulk_overwrite_global_application_commands(, commands: Any) -> None


def bulk_overwrite_guild_application_commands(, guild_id: str, commands: Any) -> None


def create_global_application_command(, name: str, description: str, options: Any, default_permission: Any, command_type: Any) -> None


def create_guild_application_command(, guild_id: str, name: str, description: str, options: Any, default_permission: Any, command_type: Any) -> None


def delete_global_application_command(, command_id: str) -> None


def delete_guild_application_command(, guild_id: str, command_id: str) -> None


def edit_application_command_permissions(, guild_id: str, command_id: Any, permissions: Any) -> None


def edit_global_application_command(, guild_id: str, command_id: str, name: Any, description: Any, options: Any, default_permissions: Any) -> None


def fetch_application() -> None


def fetch_application_command(, command_id: str) -> None


def fetch_global_application_commands() -> typing.List[EpikCord.ApplicationCommand]


def fetch_guild_application_command(, guild_id: str, command_id: str) -> None


def fetch_guild_application_command_permissions(, guild_id: str, command_id: str) -> None


def fetch_guild_application_commands(, guild_id: str) -> None



ClientMessageCommand
--------------------


ClientResponse
--------------

def close() -> None


def get_encoding() -> <class 'str'>


def json(, encoding: Any, loads: Any, content_type: Any) -> typing.Any
Read and decodes JSON response.


def raise_for_status() -> None


def read() -> <class 'bytes'>
Read response payload.


def release() -> typing.Any


def start(, connection: Any) -> ClientResponse
Start response processing.


def text(, encoding: Any, errors: str) -> <class 'str'>
Read response payload and decode.


def wait_for_close() -> None



ClientSession
-------------

def close() -> None
Close underlying connector.

Release all acquired resources.


def delete(, url: Any, kwargs: Any) -> _RequestContextManager
Perform HTTP DELETE request.


def detach() -> None
Detach connector from session without closing the former.

Session is switched to closed state anyway.


def get(, url: Any, allow_redirects: bool, kwargs: Any) -> _RequestContextManager
Perform HTTP GET request.


def head(, url: Any, allow_redirects: bool, kwargs: Any) -> _RequestContextManager
Perform HTTP HEAD request.


def options(, url: Any, allow_redirects: bool, kwargs: Any) -> _RequestContextManager
Perform HTTP OPTIONS request.


def patch(, url: Any, data: Any, kwargs: Any) -> _RequestContextManager
Perform HTTP PATCH request.


def post(, url: Any, data: Any, kwargs: Any) -> _RequestContextManager
Perform HTTP POST request.


def put(, url: Any, data: Any, kwargs: Any) -> _RequestContextManager
Perform HTTP PUT request.


def request(, method: str, url: Any, kwargs: Any) -> _RequestContextManager
Perform HTTP request.


def ws_connect(, url: Any, method: str, protocols: Any, timeout: float, receive_timeout: Any, autoclose: bool, autoping: bool, heartbeat: Any, auth: Any, origin: Any, params: Any, headers: Any, proxy: Any, proxy_auth: Any, ssl: Any, verify_ssl: Any, fingerprint: Any, ssl_context: Any, proxy_headers: Any, compress: int, max_msg_size: int) -> _WSRequestContextManager
Initiate websocket connection.



ClientSlashCommand
------------------

def option_autocomplete(, option_name: str) -> None



ClientUser
----------

def edit(, username: Any, avatar: Any) -> None


def fetch() -> None



ClientUserCommand
-----------------


ClosedWebSocketConnection
-------------------------


Colour
------

def to_rgb() -> typing.Tuple[int, int, int]
Returns an rgb color as a tuple



Colour
------

def to_rgb() -> typing.Tuple[int, int, int]
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

def add_field(, name: str, value: str, inline: bool) -> None


def set_author(, name: Any, url: Any, icon_url: Any, proxy_icon_url: Any) -> None


def set_color(, colour: Colour) -> None


def set_description(, description: Any) -> None


def set_fields(, fields: Any) -> None


def set_footer(, text: Any, icon_url: Any, proxy_icon_url: Any) -> None


def set_image(, url: Any, proxy_url: Any, height: Any, width: Any) -> None


def set_provider(, name: Any, url: Any) -> None


def set_thumbnail(, url: Any, proxy_url: Any, height: Any, width: Any) -> None


def set_timestamp(, timestamp: datetime) -> None


def set_title(, title: Any) -> None


def set_url(, url: Any) -> None


def set_video(, url: Any, proxy_url: Any, height: Any, width: Any) -> None


def to_dict() -> None



Emoji
-----

def delete(, reason: Any) -> None


def edit(, name: Any, roles: Any, reason: Any) -> None



EpikCordException
-----------------


EventHandler
------------

def channel_create(, data: dict) -> None


def component(, custom_id: str) -> None
Execute this function when a component with the `custom_id` is interacted with.


def event(, func: Any) -> None


def get_event_callback(, event_name: str, internal: Any) -> None


def guild_create(, data: Any) -> None


def guild_delete(, data: dict) -> None


def guild_member_update(, data: Any) -> None


def guild_members_chunk(, data: dict) -> None


def handle_event(, event_name: Any, data: dict) -> None


def handle_events() -> None


def interaction_create(, data: Any) -> None


def message_create(, data: dict) -> None
Event fired when messages are created


def ready(, data: dict) -> None


def voice_server_update(, data: dict) -> None


def wait_for(, event_name: str, check: Any, timeout: Any) -> None



EventsSection
-------------


FailedToConnectToVoice
----------------------


File
----


Flag
----

def calculate_from_turned() -> None



Forbidden403
------------


GateawayUnavailable502
----------------------


Guild
-----

def create_channel(, name: str, reason: Any, type: Any, topic: Any, bitrate: Any, user_limit: Any, rate_limit_per_user: Any, position: Any, permission_overwrites: Any, parent_id: Any, nsfw: Any) -> None
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


def delete() -> None


def edit(, name: Any, verification_level: Any, default_message_notifications: Any, explicit_content_filter: Any, afk_channel_id: Any, afk_timeout: Any, owner_id: Any, system_channel_id: Any, system_channel_flags: Any, rules_channel_id: Any, preferred_locale: Any, features: Any, description: Any, premium_progress_bar_enabled: Any, reason: Any) -> None
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


def fetch_channels() -> typing.List[EpikCord.GuildChannel]
Fetches the guild channels.

Returns
-------
List[GuildChannel]
    The guild channels.


def fetch_guild_preview() -> <class 'EpikCord.GuildPreview'>
Fetches the guild preview.

Returns
-------
GuildPreview
    The guild preview.



GuildApplicationCommandPermission
---------------------------------

def to_dict() -> None



GuildBan
--------


GuildChannel
------------

def create_invite(, max_age: Any, max_uses: Any, temporary: Any, unique: Any, target_type: Any, target_user_id: Any, target_application_id: Any) -> None


def delete(, reason: Any) -> None


def delete_overwrite(, overwrites: Overwrite) -> None


def fetch_invites() -> None


def fetch_pinned_messages() -> typing.List[EpikCord.Message]



GuildManager
------------

def add_to_cache(, key: Any, value: Any) -> None


def clear_cache() -> None


def fetch(, guild_id: str, skip_cache: Any, with_counts: Any) -> None


def format_cache() -> None


def get_from_cache(, key: Any) -> None


def is_in_cache(, key: Any) -> None


def remove_from_cache(, key: Any) -> None



GuildMember
-----------

def fetch_message(, message_id: str) -> <class 'EpikCord.Message'>


def fetch_messages(, around: Any, before: Any, after: Any, limit: Any) -> typing.List[EpikCord.Message]


def send(, content: Any, embeds: Any, components: Any, tts: Any, allowed_mentions: Any, sticker_ids: Any, attachments: Any, suppress_embeds: bool) -> <class 'EpikCord.Message'>



GuildNewsChannel
----------------

def bulk_delete(, message_ids: Any, reason: Any) -> None


def create_invite(, max_age: Any, max_uses: Any, temporary: Any, unique: Any, target_type: Any, target_user_id: Any, target_application_id: Any) -> None


def create_webhook(, name: str, avatar: Any, reason: Any) -> None


def delete(, reason: Any) -> None


def delete_overwrite(, overwrites: Overwrite) -> None


def fetch_invites() -> None


def fetch_message(, message_id: str) -> <class 'EpikCord.Message'>


def fetch_messages(, around: Any, before: Any, after: Any, limit: Any) -> typing.List[EpikCord.Message]


def fetch_pinned_messages() -> typing.List[EpikCord.Message]


def follow(, webhook_channel_id: str) -> None


def list_joined_private_archived_threads(, before: Any, limit: Any) -> typing.Dict[str, typing.Union[typing.List[EpikCord.Messageable], typing.List[EpikCord.ThreadMember], bool]]


def list_private_archived_threads(, before: Any, limit: Any) -> typing.Dict[str, typing.Union[typing.List[EpikCord.Messageable], typing.List[EpikCord.ThreadMember], bool]]


def list_public_archived_threads(, before: Any, limit: Any) -> typing.Dict[str, typing.Union[typing.List[EpikCord.Messageable], typing.List[EpikCord.ThreadMember], bool]]


def send(, content: Any, embeds: Any, components: Any, tts: Any, allowed_mentions: Any, sticker_ids: Any, attachments: Any, suppress_embeds: bool) -> <class 'EpikCord.Message'>


def start_thread(, name: str, auto_archive_duration: Any, type: Any, invitable: Any, rate_limit_per_user: Any, reason: Any) -> None



GuildNewsThread
---------------

def add_member(, member_id: str) -> None


def bulk_delete(, message_ids: Any, reason: Any) -> None


def create_invite(, max_age: Any, max_uses: Any, temporary: Any, unique: Any, target_type: Any, target_user_id: Any, target_application_id: Any) -> None


def create_webhook(, name: str, avatar: Any, reason: Any) -> None


def delete(, reason: Any) -> None


def delete_overwrite(, overwrites: Overwrite) -> None


def fetch_invites() -> None


def fetch_member(, member_id: str) -> <class 'EpikCord.ThreadMember'>


def fetch_message(, message_id: str) -> <class 'EpikCord.Message'>


def fetch_messages(, around: Any, before: Any, after: Any, limit: Any) -> typing.List[EpikCord.Message]


def fetch_pinned_messages() -> typing.List[EpikCord.Message]


def follow(, webhook_channel_id: str) -> None


def join() -> None


def leave() -> None


def list_joined_private_archived_threads(, before: Any, limit: Any) -> typing.Dict[str, typing.Union[typing.List[EpikCord.Messageable], typing.List[EpikCord.ThreadMember], bool]]


def list_members() -> typing.List[EpikCord.ThreadMember]


def list_private_archived_threads(, before: Any, limit: Any) -> typing.Dict[str, typing.Union[typing.List[EpikCord.Messageable], typing.List[EpikCord.ThreadMember], bool]]


def list_public_archived_threads(, before: Any, limit: Any) -> typing.Dict[str, typing.Union[typing.List[EpikCord.Messageable], typing.List[EpikCord.ThreadMember], bool]]


def remove_member(, member_id: str) -> None


def send(, content: Any, embeds: Any, components: Any, tts: Any, allowed_mentions: Any, sticker_ids: Any, attachments: Any, suppress_embeds: bool) -> <class 'EpikCord.Message'>


def start_thread(, name: str, auto_archive_duration: Any, type: Any, invitable: Any, rate_limit_per_user: Any, reason: Any) -> None



GuildPreview
------------


GuildScheduledEvent
-------------------


GuildStageChannel
-----------------


GuildTextChannel
----------------

def bulk_delete(, message_ids: Any, reason: Any) -> None


def create_invite(, max_age: Any, max_uses: Any, temporary: Any, unique: Any, target_type: Any, target_user_id: Any, target_application_id: Any) -> None


def create_webhook(, name: str, avatar: Any, reason: Any) -> None


def delete(, reason: Any) -> None


def delete_overwrite(, overwrites: Overwrite) -> None


def fetch_invites() -> None


def fetch_message(, message_id: str) -> <class 'EpikCord.Message'>


def fetch_messages(, around: Any, before: Any, after: Any, limit: Any) -> typing.List[EpikCord.Message]


def fetch_pinned_messages() -> typing.List[EpikCord.Message]


def list_joined_private_archived_threads(, before: Any, limit: Any) -> typing.Dict[str, typing.Union[typing.List[EpikCord.Messageable], typing.List[EpikCord.ThreadMember], bool]]


def list_private_archived_threads(, before: Any, limit: Any) -> typing.Dict[str, typing.Union[typing.List[EpikCord.Messageable], typing.List[EpikCord.ThreadMember], bool]]


def list_public_archived_threads(, before: Any, limit: Any) -> typing.Dict[str, typing.Union[typing.List[EpikCord.Messageable], typing.List[EpikCord.ThreadMember], bool]]


def send(, content: Any, embeds: Any, components: Any, tts: Any, allowed_mentions: Any, sticker_ids: Any, attachments: Any, suppress_embeds: bool) -> <class 'EpikCord.Message'>


def start_thread(, name: str, auto_archive_duration: Any, type: Any, invitable: Any, rate_limit_per_user: Any, reason: Any) -> None



GuildWidget
-----------


GuildWidgetSettings
-------------------


HTTPClient
----------

def close() -> None
Close underlying connector.

Release all acquired resources.


def delete(, url: Any, args: Any, to_discord: bool, kwargs: Any) -> None
Perform HTTP DELETE request.


def detach() -> None
Detach connector from session without closing the former.

Session is switched to closed state anyway.


def get(, url: Any, args: Any, to_discord: bool, kwargs: Any) -> None
Perform HTTP GET request.


def head(, url: Any, args: Any, to_discord: bool, kwargs: Any) -> None
Perform HTTP HEAD request.


def log_request(, res: Any) -> None


def options(, url: Any, allow_redirects: bool, kwargs: Any) -> _RequestContextManager
Perform HTTP OPTIONS request.


def patch(, url: Any, args: Any, to_discord: bool, kwargs: Any) -> None
Perform HTTP PATCH request.


def post(, url: Any, args: Any, to_discord: bool, kwargs: Any) -> None
Perform HTTP POST request.


def put(, url: Any, args: Any, to_discord: bool, kwargs: Any) -> None
Perform HTTP PUT request.


def request(, method: str, url: Any, kwargs: Any) -> _RequestContextManager
Perform HTTP request.


def ws_connect(, url: Any, method: str, protocols: Any, timeout: float, receive_timeout: Any, autoclose: bool, autoping: bool, heartbeat: Any, auth: Any, origin: Any, params: Any, headers: Any, proxy: Any, proxy_auth: Any, ssl: Any, verify_ssl: Any, fingerprint: Any, ssl_context: Any, proxy_headers: Any, compress: int, max_msg_size: int) -> _WSRequestContextManager
Initiate websocket connection.



IntegerOption
-------------

def to_dict() -> None



Integration
-----------


IntegrationAccount
------------------


Intents
-------

def calculate_from_turned() -> None



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

def to_dict() -> None



MentionedChannel
----------------


MentionedUser
-------------

def fetch_message(, message_id: str) -> <class 'EpikCord.Message'>


def fetch_messages(, around: Any, before: Any, after: Any, limit: Any) -> typing.List[EpikCord.Message]


def send(, content: Any, embeds: Any, components: Any, tts: Any, allowed_mentions: Any, sticker_ids: Any, attachments: Any, suppress_embeds: bool) -> <class 'EpikCord.Message'>



Message
-------

def add_reaction(, emoji: str) -> None


def crosspost() -> None


def delete() -> None


def delete_all_reactions() -> None


def delete_reaction_for_emoji(, emoji: str) -> None


def edit(, message_data: dict) -> None


def fetch_reactions(, after: Any, limit: Any) -> typing.List[EpikCord.Reaction]


def pin(, reason: Any) -> None


def remove_reaction(, emoji: str, user: Any) -> None


def start_thread(, name: str, auto_archive_duration: Any, rate_limit_per_user: Any) -> None


def unpin(, reason: Any) -> None



MessageActivity
---------------


MessageCommandInteraction
-------------------------

def create_followup(, tts: bool, content: Any, embeds: Any, allowed_mentions: Any, components: Any, attachments: Any, suppress_embeds: Any, ephemeral: Any) -> None


def defer(, show_loading_state: Any) -> None


def delete_followup() -> None


def delete_original_response() -> None


def edit_followup(, tts: bool, content: Any, embeds: Any, allowed_mentions: Any, components: Any, attachments: Any, suppress_embeds: Any, ephemeral: Any) -> None


def edit_original_response(, tts: bool, content: Any, embeds: Any, allowed_mentions: Any, components: Any, attachments: Any, suppress_embeds: Any, ephemeral: Any) -> None


def fetch_original_response(, skip_cache: Any) -> None


def is_application_command() -> None


def is_autocomplete() -> None


def is_message_component() -> None


def is_modal_submit() -> None


def is_ping() -> None


def reply(, tts: bool, content: Any, embeds: Any, allowed_mentions: Any, components: Any, attachments: Any, suppress_embeds: Any, ephemeral: Any) -> None


def send_modal(, modal: Modal) -> None



MessageComponentInteraction
---------------------------

def create_followup(, tts: bool, content: Any, embeds: Any, allowed_mentions: Any, components: Any, attachments: Any, suppress_embeds: Any, ephemeral: Any) -> None


def defer(, show_loading_state: Any) -> None


def defer_update() -> None


def delete_followup() -> None


def delete_original_response() -> None


def edit_followup(, tts: bool, content: Any, embeds: Any, allowed_mentions: Any, components: Any, attachments: Any, suppress_embeds: Any, ephemeral: Any) -> None


def edit_original_response(, tts: bool, content: Any, embeds: Any, allowed_mentions: Any, components: Any, attachments: Any, suppress_embeds: Any, ephemeral: Any) -> None


def fetch_original_response(, skip_cache: Any) -> None


def is_action_row() -> None


def is_application_command() -> None


def is_autocomplete() -> None


def is_button() -> None


def is_message_component() -> None


def is_modal_submit() -> None


def is_ping() -> None


def is_select_menu() -> None


def is_text_input() -> None


def reply(, tts: bool, content: Any, embeds: Any, allowed_mentions: Any, components: Any, attachments: Any, suppress_embeds: Any, ephemeral: Any) -> None


def send_modal(, modal: Modal) -> None


def update(, tts: bool, content: Any, embeds: Any, allowed_mentions: Any, components: Any, attachments: Any, suppress_embeds: Any) -> None



MessageInteraction
------------------


Messageable
-----------

def fetch_message(, message_id: str) -> <class 'EpikCord.Message'>


def fetch_messages(, around: Any, before: Any, after: Any, limit: Any) -> typing.List[EpikCord.Message]


def send(, content: Any, embeds: Any, components: Any, tts: Any, allowed_mentions: Any, sticker_ids: Any, attachments: Any, suppress_embeds: bool) -> <class 'EpikCord.Message'>



MethodNotAllowed405
-------------------


MissingClientSetting
--------------------


MissingCustomId
---------------


Modal
-----

def to_dict() -> None



ModalSubmitInteraction
----------------------

def create_followup(, tts: bool, content: Any, embeds: Any, allowed_mentions: Any, components: Any, attachments: Any, suppress_embeds: Any, ephemeral: Any) -> None


def defer(, show_loading_state: Any) -> None


def delete_followup() -> None


def delete_original_response() -> None


def edit_followup(, tts: bool, content: Any, embeds: Any, allowed_mentions: Any, components: Any, attachments: Any, suppress_embeds: Any, ephemeral: Any) -> None


def edit_original_response(, tts: bool, content: Any, embeds: Any, allowed_mentions: Any, components: Any, attachments: Any, suppress_embeds: Any, ephemeral: Any) -> None


def fetch_original_response(, skip_cache: Any) -> None


def is_application_command() -> None


def is_autocomplete() -> None


def is_message_component() -> None


def is_modal_submit() -> None


def is_ping() -> None


def reply(, tts: bool, content: Any, embeds: Any, allowed_mentions: Any, components: Any, attachments: Any, suppress_embeds: Any, ephemeral: Any) -> None


def send_modal(, args: Any, kwargs: Any) -> None



NotFound404
-----------


NumberOption
------------

def to_dict() -> None



Overwrite
---------


Paginator
---------

def add_page(, page: Embed) -> None


def back() -> None


def current() -> <class 'EpikCord.Embed'>


def forward() -> None


def remove_page(, page: Embed) -> None



PartialEmoji
------------

def to_dict() -> None



PartialGuild
------------


PartialUser
-----------


Permissions
-----------

def calculate_from_turned() -> None



Presence
--------

def to_dict() -> None



PrivateThread
-------------

def add_member(, member_id: str) -> None


def bulk_delete(, message_ids: Any, reason: Any) -> None


def fetch_member(, member_id: str) -> <class 'EpikCord.ThreadMember'>


def join() -> None


def leave() -> None


def list_members() -> typing.List[EpikCord.ThreadMember]


def remove_member(, member_id: str) -> None



RatelimitHandler
----------------

def is_ratelimited() -> <class 'bool'>
Checks if the client is ratelimited.


def process_headers(, headers: dict) -> None
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

def to_dict() -> None



RoleTag
-------


SelectMenu
----------

def add_options(, options: Any) -> None


def set_custom_id(, custom_id: str) -> None


def set_disabled(, disabled: bool) -> None


def set_max_values(, max: int) -> None


def set_min_values(, min: int) -> None


def set_placeholder(, placeholder: str) -> None


def to_dict() -> None



SelectMenuOption
----------------

def to_dict() -> None



Shard
-----

def change_presence(, presence: Any) -> None


def channel_create(, data: dict) -> None


def close() -> None


def component(, custom_id: str) -> None
Execute this function when a component with the `custom_id` is interacted with.


def connect() -> None


def event(, func: Any) -> None


def get_event_callback(, event_name: str, internal: Any) -> None


def guild_create(, data: Any) -> None


def guild_delete(, data: dict) -> None


def guild_member_update(, data: Any) -> None


def guild_members_chunk(, data: dict) -> None


def handle_close() -> None


def handle_event(, event_name: Any, data: dict) -> None


def handle_events() -> None


def heartbeat(, forced: Any) -> None


def identify() -> None


def interaction_create(, data: Any) -> None


def login() -> None


def message_create(, data: dict) -> None
Event fired when messages are created


def ready(, data: dict) -> None


def reconnect() -> None


def request_guild_members(, guild_id: int, query: Any, limit: Any, presences: Any, user_ids: Any, nonce: Any) -> None


def resume() -> None


def send_json(, json: dict) -> None


def voice_server_update(, data: dict) -> None


def wait_for(, event_name: str, check: Any, timeout: Any) -> None



ShardingRequired
----------------


SlashCommand
------------

def to_dict() -> None



SlashCommandOptionChoice
------------------------

def to_dict() -> None



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

def to_dict() -> None



SubCommandGroup
---------------

def to_dict() -> None



Subcommand
----------

def to_dict() -> None



SystemChannelFlags
------------------


Team
----


TeamMember
----------


TextInput
---------

def set_custom_id(, custom_id: str) -> None


def to_dict() -> None



Thread
------

def add_member(, member_id: str) -> None


def bulk_delete(, message_ids: Any, reason: Any) -> None


def fetch_member(, member_id: str) -> <class 'EpikCord.ThreadMember'>


def join() -> None


def leave() -> None


def list_members() -> typing.List[EpikCord.ThreadMember]


def remove_member(, member_id: str) -> None



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

def fetch_message(, message_id: str) -> <class 'EpikCord.Message'>


def fetch_messages(, around: Any, before: Any, after: Any, limit: Any) -> typing.List[EpikCord.Message]


def send(, content: Any, embeds: Any, components: Any, tts: Any, allowed_mentions: Any, sticker_ids: Any, attachments: Any, suppress_embeds: bool) -> <class 'EpikCord.Message'>



UserCommandInteraction
----------------------

def create_followup(, tts: bool, content: Any, embeds: Any, allowed_mentions: Any, components: Any, attachments: Any, suppress_embeds: Any, ephemeral: Any) -> None


def defer(, show_loading_state: Any) -> None


def delete_followup() -> None


def delete_original_response() -> None


def edit_followup(, tts: bool, content: Any, embeds: Any, allowed_mentions: Any, components: Any, attachments: Any, suppress_embeds: Any, ephemeral: Any) -> None


def edit_original_response(, tts: bool, content: Any, embeds: Any, allowed_mentions: Any, components: Any, attachments: Any, suppress_embeds: Any, ephemeral: Any) -> None


def fetch_original_response(, skip_cache: Any) -> None


def is_application_command() -> None


def is_autocomplete() -> None


def is_message_component() -> None


def is_modal_submit() -> None


def is_ping() -> None


def reply(, tts: bool, content: Any, embeds: Any, allowed_mentions: Any, components: Any, attachments: Any, suppress_embeds: Any, ephemeral: Any) -> None


def send_modal(, modal: Modal) -> None



UserOption
----------

def to_dict() -> None



Utils
-----

def cancel_tasks(, loop: Any) -> None


def channel_from_type(, channel_data: dict) -> None


def cleanup_loop(, loop: Any) -> None


def component_from_type(, component_data: dict) -> None


def compute_timedelta(, dt: datetime) -> None


def escape_markdown(, text: str, as_needed: bool, ignore_links: bool) -> <class 'str'>


def escape_mentions(, text: str) -> <class 'str'>


def get_mime_type_for_image(, data: bytes) -> None


def interaction_from_type(, data: Any) -> None


def remove_markdown(, text: str, ignore_links: bool) -> <class 'str'>


def sleep_until(, when: Any, result: Any) -> typing.Optional[~T]


def utcnow() -> <class 'datetime.datetime'>



VoiceChannel
------------

def create_invite(, max_age: Any, max_uses: Any, temporary: Any, unique: Any, target_type: Any, target_user_id: Any, target_application_id: Any) -> None


def delete(, reason: Any) -> None


def delete_overwrite(, overwrites: Overwrite) -> None


def fetch_invites() -> None


def fetch_pinned_messages() -> typing.List[EpikCord.Message]



VoiceState
----------


VoiceWebsocketClient
--------------------

def connect(, muted: Any, deafened: Any) -> None



Webhook
-------


WebhookUser
-----------


WebsocketClient
---------------

def change_presence(, presence: Any) -> None


def channel_create(, data: dict) -> None


def close() -> None


def component(, custom_id: str) -> None
Execute this function when a component with the `custom_id` is interacted with.


def connect() -> None


def event(, func: Any) -> None


def get_event_callback(, event_name: str, internal: Any) -> None


def guild_create(, data: Any) -> None


def guild_delete(, data: dict) -> None


def guild_member_update(, data: Any) -> None


def guild_members_chunk(, data: dict) -> None


def handle_close() -> None


def handle_event(, event_name: Any, data: dict) -> None


def handle_events() -> None


def heartbeat(, forced: Any) -> None


def identify() -> None


def interaction_create(, data: Any) -> None


def login() -> None


def message_create(, data: dict) -> None
Event fired when messages are created


def ready(, data: dict) -> None


def reconnect() -> None


def request_guild_members(, guild_id: int, query: Any, limit: Any, presences: Any, user_ids: Any, nonce: Any) -> None


def resume() -> None


def send_json(, json: dict) -> None


def voice_server_update(, data: dict) -> None


def wait_for(, event_name: str, check: Any, timeout: Any) -> None



WelcomeScreen
-------------


WelcomeScreenChannel
--------------------
