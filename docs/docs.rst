

ActionRow
---------

def add_components(self: Any, components: typing.List[typing.Union[EpikCord.components.Button, EpikCord.components.SelectMenu]]) -> <class 'inspect._empty'>

def to_dict(self: Any) -> <class 'inspect._empty'>


Activity
--------

def to_dict(self: Any) -> <class 'inspect._empty'>Returns activity class as dict

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

def create_followup(self: Any, tts: <class 'bool'>, content: typing.Optional[str], embeds: typing.Optional[typing.List[EpikCord.Embed]], allowed_mentions: Any, components: typing.Optional[typing.List[typing.Union[EpikCord.components.Button, EpikCord.components.SelectMenu, EpikCord.components.TextInput]]], attachments: typing.Optional[typing.List[EpikCord.Attachment]], suppress_embeds: typing.Optional[bool], ephemeral: typing.Optional[bool]) -> None

def defer(self: Any, show_loading_state: typing.Optional[bool]) -> <class 'inspect._empty'>

def delete_followup(self: Any) -> <class 'inspect._empty'>

def delete_original_response(self: Any) -> <class 'inspect._empty'>

def edit_followup(self: Any, tts: <class 'bool'>, content: typing.Optional[str], embeds: typing.Optional[typing.List[EpikCord.Embed]], allowed_mentions: Any, components: typing.Optional[typing.List[typing.Union[EpikCord.components.Button, EpikCord.components.SelectMenu, EpikCord.components.TextInput]]], attachments: typing.Optional[typing.List[EpikCord.Attachment]], suppress_embeds: typing.Optional[bool], ephemeral: typing.Optional[bool]) -> None

def edit_original_response(self: Any, tts: <class 'bool'>, content: typing.Optional[str], embeds: typing.Optional[typing.List[EpikCord.Embed]], allowed_mentions: Any, components: typing.Optional[typing.List[typing.Union[EpikCord.components.Button, EpikCord.components.SelectMenu, EpikCord.components.TextInput]]], attachments: typing.Optional[typing.List[EpikCord.Attachment]], suppress_embeds: typing.Optional[bool], ephemeral: typing.Optional[bool]) -> None

def fetch_original_response(self: Any, skip_cache: typing.Optional[bool]) -> <class 'inspect._empty'>

def is_application_command(self: Any) -> <class 'inspect._empty'>

def is_autocomplete(self: Any) -> <class 'inspect._empty'>

def is_message_component(self: Any) -> <class 'inspect._empty'>

def is_modal_submit(self: Any) -> <class 'inspect._empty'>

def is_ping(self: Any) -> <class 'inspect._empty'>

def reply(self: Any, tts: <class 'bool'>, content: typing.Optional[str], embeds: typing.Optional[typing.List[EpikCord.Embed]], allowed_mentions: Any, components: typing.Optional[typing.List[typing.Union[EpikCord.components.Button, EpikCord.components.SelectMenu, EpikCord.components.TextInput]]], attachments: typing.Optional[typing.List[EpikCord.Attachment]], suppress_embeds: typing.Optional[bool], ephemeral: typing.Optional[bool]) -> None

def send_modal(self: Any, modal: <class 'EpikCord.Modal'>) -> <class 'inspect._empty'>


ApplicationCommandOption
------------------------


ApplicationCommandPermission
----------------------------

def to_dict(self: Any) -> <class 'inspect._empty'>


ApplicationCommandSubcommandOption
----------------------------------


Attachment
----------


AttachmentOption
----------------

def to_dict(self: Any) -> <class 'inspect._empty'>


AutoCompleteInteraction
-----------------------

def create_followup(self: Any, tts: <class 'bool'>, content: typing.Optional[str], embeds: typing.Optional[typing.List[EpikCord.Embed]], allowed_mentions: Any, components: typing.Optional[typing.List[typing.Union[EpikCord.components.Button, EpikCord.components.SelectMenu, EpikCord.components.TextInput]]], attachments: typing.Optional[typing.List[EpikCord.Attachment]], suppress_embeds: typing.Optional[bool], ephemeral: typing.Optional[bool]) -> None

def defer(self: Any, show_loading_state: typing.Optional[bool]) -> <class 'inspect._empty'>

def delete_followup(self: Any) -> <class 'inspect._empty'>

def delete_original_response(self: Any) -> <class 'inspect._empty'>

def edit_followup(self: Any, tts: <class 'bool'>, content: typing.Optional[str], embeds: typing.Optional[typing.List[EpikCord.Embed]], allowed_mentions: Any, components: typing.Optional[typing.List[typing.Union[EpikCord.components.Button, EpikCord.components.SelectMenu, EpikCord.components.TextInput]]], attachments: typing.Optional[typing.List[EpikCord.Attachment]], suppress_embeds: typing.Optional[bool], ephemeral: typing.Optional[bool]) -> None

def edit_original_response(self: Any, tts: <class 'bool'>, content: typing.Optional[str], embeds: typing.Optional[typing.List[EpikCord.Embed]], allowed_mentions: Any, components: typing.Optional[typing.List[typing.Union[EpikCord.components.Button, EpikCord.components.SelectMenu, EpikCord.components.TextInput]]], attachments: typing.Optional[typing.List[EpikCord.Attachment]], suppress_embeds: typing.Optional[bool], ephemeral: typing.Optional[bool]) -> None

def fetch_original_response(self: Any, skip_cache: typing.Optional[bool]) -> <class 'inspect._empty'>

def is_application_command(self: Any) -> <class 'inspect._empty'>

def is_autocomplete(self: Any) -> <class 'inspect._empty'>

def is_message_component(self: Any) -> <class 'inspect._empty'>

def is_modal_submit(self: Any) -> <class 'inspect._empty'>

def is_ping(self: Any) -> <class 'inspect._empty'>

def reply(self: Any, choices: typing.List[EpikCord.options.SlashCommandOptionChoice]) -> None

def send_modal(self: Any, modal: <class 'EpikCord.Modal'>) -> <class 'inspect._empty'>


BadRequest400
-------------


BaseChannel
-----------


BaseComponent
-------------

def set_custom_id(self: Any, custom_id: <class 'str'>) -> <class 'inspect._empty'>


BaseInteraction
---------------

def create_followup(self: Any, tts: <class 'bool'>, content: typing.Optional[str], embeds: typing.Optional[typing.List[EpikCord.Embed]], allowed_mentions: Any, components: typing.Optional[typing.List[typing.Union[EpikCord.components.Button, EpikCord.components.SelectMenu, EpikCord.components.TextInput]]], attachments: typing.Optional[typing.List[EpikCord.Attachment]], suppress_embeds: typing.Optional[bool], ephemeral: typing.Optional[bool]) -> None

def defer(self: Any, show_loading_state: typing.Optional[bool]) -> <class 'inspect._empty'>

def delete_followup(self: Any) -> <class 'inspect._empty'>

def delete_original_response(self: Any) -> <class 'inspect._empty'>

def edit_followup(self: Any, tts: <class 'bool'>, content: typing.Optional[str], embeds: typing.Optional[typing.List[EpikCord.Embed]], allowed_mentions: Any, components: typing.Optional[typing.List[typing.Union[EpikCord.components.Button, EpikCord.components.SelectMenu, EpikCord.components.TextInput]]], attachments: typing.Optional[typing.List[EpikCord.Attachment]], suppress_embeds: typing.Optional[bool], ephemeral: typing.Optional[bool]) -> None

def edit_original_response(self: Any, tts: <class 'bool'>, content: typing.Optional[str], embeds: typing.Optional[typing.List[EpikCord.Embed]], allowed_mentions: Any, components: typing.Optional[typing.List[typing.Union[EpikCord.components.Button, EpikCord.components.SelectMenu, EpikCord.components.TextInput]]], attachments: typing.Optional[typing.List[EpikCord.Attachment]], suppress_embeds: typing.Optional[bool], ephemeral: typing.Optional[bool]) -> None

def fetch_original_response(self: Any, skip_cache: typing.Optional[bool]) -> <class 'inspect._empty'>

def is_application_command(self: Any) -> <class 'inspect._empty'>

def is_autocomplete(self: Any) -> <class 'inspect._empty'>

def is_message_component(self: Any) -> <class 'inspect._empty'>

def is_modal_submit(self: Any) -> <class 'inspect._empty'>

def is_ping(self: Any) -> <class 'inspect._empty'>

def reply(self: Any, tts: <class 'bool'>, content: typing.Optional[str], embeds: typing.Optional[typing.List[EpikCord.Embed]], allowed_mentions: Any, components: typing.Optional[typing.List[typing.Union[EpikCord.components.Button, EpikCord.components.SelectMenu, EpikCord.components.TextInput]]], attachments: typing.Optional[typing.List[EpikCord.Attachment]], suppress_embeds: typing.Optional[bool], ephemeral: typing.Optional[bool]) -> None

def send_modal(self: Any, modal: <class 'EpikCord.Modal'>) -> <class 'inspect._empty'>


BaseSlashCommandOption
----------------------

def to_dict(self: Any) -> <class 'inspect._empty'>


BooleanOption
-------------

def to_dict(self: Any) -> <class 'inspect._empty'>


Button
------

def set_custom_id(self: Any, custom_id: <class 'str'>) -> <class 'inspect._empty'>

def set_emoji(self: Any, emoji: typing.Union[EpikCord.partials.PartialEmoji, dict]) -> <class 'inspect._empty'>

def set_label(self: Any, label: <class 'str'>) -> <class 'inspect._empty'>

def set_style(self: Any, style: typing.Union[int, str]) -> <class 'inspect._empty'>

def set_url(self: Any, url: <class 'str'>) -> <class 'inspect._empty'>

def to_dict(self: Any) -> <class 'inspect._empty'>


CacheManager
------------

def add_to_cache(self: Any, key: Any, value: Any) -> <class 'inspect._empty'>

def clear_cache(self: Any) -> <class 'inspect._empty'>

def get_from_cache(self: Any, key: Any) -> <class 'inspect._empty'>

def is_in_cache(self: Any, key: Any) -> <class 'inspect._empty'>

def remove_from_cache(self: Any, key: Any) -> <class 'inspect._empty'>


ChannelCategory
---------------

def create_invite(self: Any, max_age: typing.Optional[int], max_uses: typing.Optional[int], temporary: typing.Optional[bool], unique: typing.Optional[bool], target_type: typing.Optional[int], target_user_id: typing.Optional[str], target_application_id: typing.Optional[str]) -> <class 'inspect._empty'>

def delete(self: Any, reason: typing.Optional[str]) -> None

def delete_overwrite(self: Any, overwrites: <class 'EpikCord.Overwrite'>) -> None

def fetch_invites(self: Any) -> <class 'inspect._empty'>

def fetch_pinned_messages(self: Any) -> typing.List[EpikCord.Message]


ChannelManager
--------------

def add_to_cache(self: Any, key: Any, value: Any) -> <class 'inspect._empty'>

def clear_cache(self: Any) -> <class 'inspect._empty'>

def fetch(self: Any, channel_id: Any, skip_cache: typing.Optional[bool]) -> <class 'inspect._empty'>

def format_cache(self: Any) -> <class 'inspect._empty'>

def get_from_cache(self: Any, key: Any) -> <class 'inspect._empty'>

def is_in_cache(self: Any, key: Any) -> <class 'inspect._empty'>

def remove_from_cache(self: Any, key: Any) -> <class 'inspect._empty'>


ChannelOption
-------------

def to_dict(self: Any) -> <class 'inspect._empty'>


ChannelOptionChannelTypes
-------------------------


Client
------

def add_section(self: Any, section: typing.Union[EpikCord.CommandsSection, EpikCord.EventsSection]) -> <class 'inspect._empty'>

def change_presence(self: Any, presence: typing.Optional[EpikCord.Presence]) -> <class 'inspect._empty'>

def channel_create(self: Any, data: <class 'dict'>) -> <class 'inspect._empty'>

def close(self: Any) -> None

def command(self: Any, name: typing.Optional[str], description: typing.Optional[str], guild_ids: typing.Optional[typing.List[str]], options: typing.Union[EpikCord.options.Subcommand, EpikCord.options.SubCommandGroup, EpikCord.options.StringOption, EpikCord.options.IntegerOption, EpikCord.options.BooleanOption, EpikCord.options.UserOption, EpikCord.options.ChannelOption, EpikCord.options.RoleOption, EpikCord.options.MentionableOption, EpikCord.options.NumberOption, NoneType]) -> <class 'inspect._empty'>

def component(self: Any, custom_id: <class 'str'>) -> <class 'inspect._empty'>Execute this function when a component with the `custom_id` is interacted with.


def connect(self: Any) -> <class 'inspect._empty'>

def event(self: Any, func: Any) -> <class 'inspect._empty'>

def get_event_callback(self: Any, event_name: <class 'str'>, internal: Any) -> <class 'inspect._empty'>

def guild_create(self: Any, data: Any) -> <class 'inspect._empty'>

def guild_delete(self: Any, data: <class 'dict'>) -> <class 'inspect._empty'>

def guild_member_update(self: Any, data: Any) -> <class 'inspect._empty'>

def guild_members_chunk(self: Any, data: <class 'dict'>) -> <class 'inspect._empty'>

def handle_close(self: Any) -> <class 'inspect._empty'>

def handle_event(self: Any, event_name: typing.Optional[str], data: <class 'dict'>) -> <class 'inspect._empty'>

def handle_events(self: Any) -> <class 'inspect._empty'>

def heartbeat(self: Any, forced: typing.Optional[bool]) -> <class 'inspect._empty'>

def identify(self: Any) -> <class 'inspect._empty'>

def interaction_create(self: Any, data: Any) -> <class 'inspect._empty'>

def login(self: Any) -> <class 'inspect._empty'>

def message_command(self: Any, name: typing.Optional[str]) -> <class 'inspect._empty'>

def message_create(self: Any, data: <class 'dict'>) -> <class 'inspect._empty'>Event fired when messages are created


def ready(self: Any, data: <class 'dict'>) -> <class 'inspect._empty'>

def reconnect(self: Any) -> <class 'inspect._empty'>

def request_guild_members(self: Any, guild_id: <class 'int'>, query: typing.Optional[str], limit: typing.Optional[int], presences: typing.Optional[bool], user_ids: typing.Optional[typing.List[str]], nonce: typing.Optional[str]) -> <class 'inspect._empty'>

def resume(self: Any) -> <class 'inspect._empty'>

def send_json(self: Any, json: <class 'dict'>) -> <class 'inspect._empty'>

def unload_section(self: Any, section: typing.Union[EpikCord.CommandsSection, EpikCord.EventsSection]) -> <class 'inspect._empty'>

def user_command(self: Any, name: typing.Optional[str]) -> <class 'inspect._empty'>

def voice_server_update(self: Any, data: <class 'dict'>) -> <class 'inspect._empty'>

def wait_for(self: Any, event_name: <class 'str'>, check: typing.Optional[<built-in function callable>], timeout: typing.Union[float, int, NoneType]) -> <class 'inspect._empty'>


ClientApplication
-----------------

def bulk_overwrite_global_application_commands(self: Any, commands: typing.List[EpikCord.ApplicationCommand]) -> <class 'inspect._empty'>

def bulk_overwrite_guild_application_commands(self: Any, guild_id: <class 'str'>, commands: typing.List[EpikCord.ApplicationCommand]) -> <class 'inspect._empty'>

def create_global_application_command(self: Any, name: <class 'str'>, description: <class 'str'>, options: typing.Optional[typing.List[typing.Union[EpikCord.options.Subcommand, EpikCord.options.SubCommandGroup, EpikCord.options.StringOption, EpikCord.options.IntegerOption, EpikCord.options.BooleanOption, EpikCord.options.UserOption, EpikCord.options.ChannelOption, EpikCord.options.RoleOption, EpikCord.options.MentionableOption, EpikCord.options.NumberOption]]], default_permission: typing.Optional[bool], command_type: typing.Optional[int]) -> <class 'inspect._empty'>

def create_guild_application_command(self: Any, guild_id: <class 'str'>, name: <class 'str'>, description: <class 'str'>, options: typing.Optional[typing.List[typing.Union[EpikCord.options.Subcommand, EpikCord.options.SubCommandGroup, EpikCord.options.StringOption, EpikCord.options.IntegerOption, EpikCord.options.BooleanOption, EpikCord.options.UserOption, EpikCord.options.ChannelOption, EpikCord.options.RoleOption, EpikCord.options.MentionableOption, EpikCord.options.NumberOption]]], default_permission: typing.Optional[bool], command_type: typing.Optional[int]) -> <class 'inspect._empty'>

def delete_global_application_command(self: Any, command_id: <class 'str'>) -> <class 'inspect._empty'>

def delete_guild_application_command(self: Any, guild_id: <class 'str'>, command_id: <class 'str'>) -> <class 'inspect._empty'>

def edit_application_command_permissions(self: Any, guild_id: <class 'str'>, command_id: Any, permissions: typing.List[EpikCord.ApplicationCommandPermission]) -> <class 'inspect._empty'>

def edit_global_application_command(self: Any, guild_id: <class 'str'>, command_id: <class 'str'>, name: typing.Optional[str], description: typing.Optional[str], options: typing.Optional[typing.List[typing.Union[EpikCord.options.Subcommand, EpikCord.options.SubCommandGroup, EpikCord.options.StringOption, EpikCord.options.IntegerOption, EpikCord.options.BooleanOption, EpikCord.options.UserOption, EpikCord.options.ChannelOption, EpikCord.options.RoleOption, EpikCord.options.MentionableOption, EpikCord.options.NumberOption]]], default_permissions: typing.Optional[bool]) -> <class 'inspect._empty'>

def fetch_application(self: Any) -> <class 'inspect._empty'>

def fetch_application_command(self: Any, command_id: <class 'str'>) -> <class 'inspect._empty'>

def fetch_global_application_commands(self: Any) -> typing.List[EpikCord.ApplicationCommand]

def fetch_guild_application_command(self: Any, guild_id: <class 'str'>, command_id: <class 'str'>) -> <class 'inspect._empty'>

def fetch_guild_application_command_permissions(self: Any, guild_id: <class 'str'>, command_id: <class 'str'>) -> <class 'inspect._empty'>

def fetch_guild_application_commands(self: Any, guild_id: <class 'str'>) -> <class 'inspect._empty'>


ClientMessageCommand
--------------------


ClientResponse
--------------

def close(self: Any) -> None

def get_encoding(self: Any) -> <class 'str'>

def json(self: Any, encoding: typing.Optional[str], loads: typing.Callable[[str], typing.Any], content_type: typing.Optional[str]) -> typing.AnyRead and decodes JSON response.


def raise_for_status(self: Any) -> None

def read(self: Any) -> <class 'bytes'>Read response payload.


def release(self: Any) -> typing.Any

def start(self: Any, connection: Connection) -> ClientResponseStart response processing.


def text(self: Any, encoding: typing.Optional[str], errors: <class 'str'>) -> <class 'str'>Read response payload and decode.


def wait_for_close(self: Any) -> None


ClientSession
-------------

def close(self: Any) -> NoneClose underlying connector.

Release all acquired resources.


def delete(self: Any, url: typing.Union[str, yarl.URL], kwargs: typing.Any) -> _RequestContextManagerPerform HTTP DELETE request.


def detach(self: Any) -> NoneDetach connector from session without closing the former.

Session is switched to closed state anyway.


def get(self: Any, url: typing.Union[str, yarl.URL], allow_redirects: <class 'bool'>, kwargs: typing.Any) -> _RequestContextManagerPerform HTTP GET request.


def head(self: Any, url: typing.Union[str, yarl.URL], allow_redirects: <class 'bool'>, kwargs: typing.Any) -> _RequestContextManagerPerform HTTP HEAD request.


def options(self: Any, url: typing.Union[str, yarl.URL], allow_redirects: <class 'bool'>, kwargs: typing.Any) -> _RequestContextManagerPerform HTTP OPTIONS request.


def patch(self: Any, url: typing.Union[str, yarl.URL], data: typing.Any, kwargs: typing.Any) -> _RequestContextManagerPerform HTTP PATCH request.


def post(self: Any, url: typing.Union[str, yarl.URL], data: typing.Any, kwargs: typing.Any) -> _RequestContextManagerPerform HTTP POST request.


def put(self: Any, url: typing.Union[str, yarl.URL], data: typing.Any, kwargs: typing.Any) -> _RequestContextManagerPerform HTTP PUT request.


def request(self: Any, method: <class 'str'>, url: typing.Union[str, yarl.URL], kwargs: typing.Any) -> _RequestContextManagerPerform HTTP request.


def ws_connect(self: Any, url: typing.Union[str, yarl.URL], method: <class 'str'>, protocols: typing.Iterable[str], timeout: <class 'float'>, receive_timeout: typing.Optional[float], autoclose: <class 'bool'>, autoping: <class 'bool'>, heartbeat: typing.Optional[float], auth: typing.Optional[aiohttp.helpers.BasicAuth], origin: typing.Optional[str], params: typing.Optional[typing.Mapping[str, str]], headers: typing.Union[typing.Mapping[typing.Union[str, multidict._multidict.istr], str], multidict._multidict.CIMultiDict, multidict._multidict.CIMultiDictProxy, NoneType], proxy: typing.Union[str, yarl.URL, NoneType], proxy_auth: typing.Optional[aiohttp.helpers.BasicAuth], ssl: typing.Union[ssl.SSLContext, bool, NoneType, aiohttp.client_reqrep.Fingerprint], verify_ssl: typing.Optional[bool], fingerprint: typing.Optional[bytes], ssl_context: typing.Optional[ssl.SSLContext], proxy_headers: typing.Union[typing.Mapping[typing.Union[str, multidict._multidict.istr], str], multidict._multidict.CIMultiDict, multidict._multidict.CIMultiDictProxy, NoneType], compress: <class 'int'>, max_msg_size: <class 'int'>) -> _WSRequestContextManagerInitiate websocket connection.



ClientSlashCommand
------------------

def option_autocomplete(self: Any, option_name: <class 'str'>) -> <class 'inspect._empty'>


ClientUser
----------

def edit(self: Any, username: typing.Optional[str], avatar: typing.Optional[bytes]) -> <class 'inspect._empty'>

def fetch(self: Any) -> <class 'inspect._empty'>


ClientUserCommand
-----------------


ClosedWebSocketConnection
-------------------------


Colour
------

def to_rgb(self: Any) -> typing.Tuple[int, int, int]Returns an rgb color as a tuple



Colour
------

def to_rgb(self: Any) -> typing.Tuple[int, int, int]Returns an rgb color as a tuple



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

def add_field(self: Any, name: <class 'str'>, value: <class 'str'>, inline: <class 'bool'>) -> <class 'inspect._empty'>

def set_author(self: Any, name: typing.Optional[str], url: typing.Optional[str], icon_url: typing.Optional[str], proxy_icon_url: typing.Optional[str]) -> <class 'inspect._empty'>

def set_color(self: Any, colour: <class 'EpikCord.Colour'>) -> <class 'inspect._empty'>

def set_description(self: Any, description: typing.Optional[str]) -> <class 'inspect._empty'>

def set_fields(self: Any, fields: typing.List[dict]) -> <class 'inspect._empty'>

def set_footer(self: Any, text: typing.Optional[str], icon_url: typing.Optional[str], proxy_icon_url: typing.Optional[str]) -> <class 'inspect._empty'>

def set_image(self: Any, url: typing.Optional[str], proxy_url: typing.Optional[str], height: typing.Optional[int], width: typing.Optional[int]) -> <class 'inspect._empty'>

def set_provider(self: Any, name: typing.Optional[str], url: typing.Optional[str]) -> <class 'inspect._empty'>

def set_thumbnail(self: Any, url: typing.Optional[str], proxy_url: typing.Optional[str], height: typing.Optional[int], width: typing.Optional[int]) -> <class 'inspect._empty'>

def set_timestamp(self: Any, timestamp: <class 'datetime.datetime'>) -> <class 'inspect._empty'>

def set_title(self: Any, title: typing.Optional[str]) -> <class 'inspect._empty'>

def set_url(self: Any, url: typing.Optional[str]) -> <class 'inspect._empty'>

def set_video(self: Any, url: typing.Optional[str], proxy_url: typing.Optional[str], height: typing.Optional[int], width: typing.Optional[int]) -> <class 'inspect._empty'>

def to_dict(self: Any) -> <class 'inspect._empty'>


Emoji
-----

def delete(self: Any, reason: typing.Optional[str]) -> <class 'inspect._empty'>

def edit(self: Any, name: typing.Optional[str], roles: typing.Optional[typing.List[EpikCord.Role]], reason: typing.Optional[str]) -> <class 'inspect._empty'>


EpikCordException
-----------------


EventHandler
------------

def channel_create(self: Any, data: <class 'dict'>) -> <class 'inspect._empty'>

def component(self: Any, custom_id: <class 'str'>) -> <class 'inspect._empty'>Execute this function when a component with the `custom_id` is interacted with.


def event(self: Any, func: Any) -> <class 'inspect._empty'>

def get_event_callback(self: Any, event_name: <class 'str'>, internal: Any) -> <class 'inspect._empty'>

def guild_create(self: Any, data: Any) -> <class 'inspect._empty'>

def guild_delete(self: Any, data: <class 'dict'>) -> <class 'inspect._empty'>

def guild_member_update(self: Any, data: Any) -> <class 'inspect._empty'>

def guild_members_chunk(self: Any, data: <class 'dict'>) -> <class 'inspect._empty'>

def handle_event(self: Any, event_name: typing.Optional[str], data: <class 'dict'>) -> <class 'inspect._empty'>

def handle_events(self: Any) -> <class 'inspect._empty'>

def interaction_create(self: Any, data: Any) -> <class 'inspect._empty'>

def message_create(self: Any, data: <class 'dict'>) -> <class 'inspect._empty'>Event fired when messages are created


def ready(self: Any, data: <class 'dict'>) -> <class 'inspect._empty'>

def voice_server_update(self: Any, data: <class 'dict'>) -> <class 'inspect._empty'>

def wait_for(self: Any, event_name: <class 'str'>, check: typing.Optional[<built-in function callable>], timeout: typing.Union[float, int, NoneType]) -> <class 'inspect._empty'>


EventsSection
-------------


FailedToConnectToVoice
----------------------


File
----


Flag
----

def calculate_from_turned(self: Any) -> <class 'inspect._empty'>


Forbidden403
------------


GateawayUnavailable502
----------------------


Guild
-----

def create_channel(self: Any, name: <class 'str'>, reason: typing.Optional[str], type: typing.Optional[int], topic: typing.Optional[str], bitrate: typing.Optional[int], user_limit: typing.Optional[int], rate_limit_per_user: typing.Optional[int], position: typing.Optional[int], permission_overwrites: typing.List[typing.Optional[EpikCord.Overwrite]], parent_id: typing.Optional[str], nsfw: typing.Optional[bool]) -> <class 'inspect._empty'>Creates a channel.

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


def delete(self: Any) -> <class 'inspect._empty'>

def edit(self: Any, name: typing.Optional[str], verification_level: typing.Optional[int], default_message_notifications: typing.Optional[int], explicit_content_filter: typing.Optional[int], afk_channel_id: typing.Optional[str], afk_timeout: typing.Optional[int], owner_id: typing.Optional[str], system_channel_id: typing.Optional[str], system_channel_flags: typing.Optional[EpikCord.SystemChannelFlags], rules_channel_id: typing.Optional[str], preferred_locale: typing.Optional[str], features: typing.Optional[typing.List[str]], description: typing.Optional[str], premium_progress_bar_enabled: typing.Optional[bool], reason: typing.Optional[str]) -> <class 'inspect._empty'>Edits the guild.

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


def fetch_channels(self: Any) -> typing.List[EpikCord.GuildChannel]Fetches the guild channels.

Returns
-------
List[GuildChannel]
    The guild channels.


def fetch_guild_preview(self: Any) -> <class 'EpikCord.GuildPreview'>Fetches the guild preview.

Returns
-------
GuildPreview
    The guild preview.



GuildApplicationCommandPermission
---------------------------------

def to_dict(self: Any) -> <class 'inspect._empty'>


GuildBan
--------


GuildChannel
------------

def create_invite(self: Any, max_age: typing.Optional[int], max_uses: typing.Optional[int], temporary: typing.Optional[bool], unique: typing.Optional[bool], target_type: typing.Optional[int], target_user_id: typing.Optional[str], target_application_id: typing.Optional[str]) -> <class 'inspect._empty'>

def delete(self: Any, reason: typing.Optional[str]) -> None

def delete_overwrite(self: Any, overwrites: <class 'EpikCord.Overwrite'>) -> None

def fetch_invites(self: Any) -> <class 'inspect._empty'>

def fetch_pinned_messages(self: Any) -> typing.List[EpikCord.Message]


GuildManager
------------

def add_to_cache(self: Any, key: Any, value: Any) -> <class 'inspect._empty'>

def clear_cache(self: Any) -> <class 'inspect._empty'>

def fetch(self: Any, guild_id: <class 'str'>, skip_cache: typing.Optional[bool], with_counts: typing.Optional[bool]) -> <class 'inspect._empty'>

def format_cache(self: Any) -> <class 'inspect._empty'>

def get_from_cache(self: Any, key: Any) -> <class 'inspect._empty'>

def is_in_cache(self: Any, key: Any) -> <class 'inspect._empty'>

def remove_from_cache(self: Any, key: Any) -> <class 'inspect._empty'>


GuildMember
-----------

def fetch_message(self: Any, message_id: <class 'str'>) -> <class 'EpikCord.Message'>

def fetch_messages(self: Any, around: typing.Optional[str], before: typing.Optional[str], after: typing.Optional[str], limit: typing.Optional[int]) -> typing.List[EpikCord.Message]

def send(self: Any, content: typing.Optional[str], embeds: typing.Optional[typing.List[dict]], components: Any, tts: typing.Optional[bool], allowed_mentions: Any, sticker_ids: typing.Optional[typing.List[str]], attachments: typing.List[EpikCord.File], suppress_embeds: <class 'bool'>) -> <class 'EpikCord.Message'>


GuildNewsChannel
----------------

def bulk_delete(self: Any, message_ids: typing.List[str], reason: typing.Optional[str]) -> None

def create_invite(self: Any, max_age: typing.Optional[int], max_uses: typing.Optional[int], temporary: typing.Optional[bool], unique: typing.Optional[bool], target_type: typing.Optional[int], target_user_id: typing.Optional[str], target_application_id: typing.Optional[str]) -> <class 'inspect._empty'>

def create_webhook(self: Any, name: <class 'str'>, avatar: typing.Optional[str], reason: typing.Optional[str]) -> <class 'inspect._empty'>

def delete(self: Any, reason: typing.Optional[str]) -> None

def delete_overwrite(self: Any, overwrites: <class 'EpikCord.Overwrite'>) -> None

def fetch_invites(self: Any) -> <class 'inspect._empty'>

def fetch_message(self: Any, message_id: <class 'str'>) -> <class 'EpikCord.Message'>

def fetch_messages(self: Any, around: typing.Optional[str], before: typing.Optional[str], after: typing.Optional[str], limit: typing.Optional[int]) -> typing.List[EpikCord.Message]

def fetch_pinned_messages(self: Any) -> typing.List[EpikCord.Message]

def follow(self: Any, webhook_channel_id: <class 'str'>) -> <class 'inspect._empty'>

def list_joined_private_archived_threads(self: Any, before: typing.Optional[str], limit: typing.Optional[int]) -> typing.Dict[str, typing.Union[typing.List[EpikCord.Messageable], typing.List[EpikCord.ThreadMember], bool]]

def list_private_archived_threads(self: Any, before: typing.Optional[str], limit: typing.Optional[int]) -> typing.Dict[str, typing.Union[typing.List[EpikCord.Messageable], typing.List[EpikCord.ThreadMember], bool]]

def list_public_archived_threads(self: Any, before: typing.Optional[str], limit: typing.Optional[int]) -> typing.Dict[str, typing.Union[typing.List[EpikCord.Messageable], typing.List[EpikCord.ThreadMember], bool]]

def send(self: Any, content: typing.Optional[str], embeds: typing.Optional[typing.List[dict]], components: Any, tts: typing.Optional[bool], allowed_mentions: Any, sticker_ids: typing.Optional[typing.List[str]], attachments: typing.List[EpikCord.File], suppress_embeds: <class 'bool'>) -> <class 'EpikCord.Message'>

def start_thread(self: Any, name: <class 'str'>, auto_archive_duration: typing.Optional[int], type: typing.Optional[int], invitable: typing.Optional[bool], rate_limit_per_user: typing.Optional[int], reason: typing.Optional[str]) -> <class 'inspect._empty'>


GuildNewsThread
---------------

def add_member(self: Any, member_id: <class 'str'>) -> <class 'inspect._empty'>

def bulk_delete(self: Any, message_ids: typing.List[str], reason: typing.Optional[str]) -> None

def create_invite(self: Any, max_age: typing.Optional[int], max_uses: typing.Optional[int], temporary: typing.Optional[bool], unique: typing.Optional[bool], target_type: typing.Optional[int], target_user_id: typing.Optional[str], target_application_id: typing.Optional[str]) -> <class 'inspect._empty'>

def create_webhook(self: Any, name: <class 'str'>, avatar: typing.Optional[str], reason: typing.Optional[str]) -> <class 'inspect._empty'>

def delete(self: Any, reason: typing.Optional[str]) -> None

def delete_overwrite(self: Any, overwrites: <class 'EpikCord.Overwrite'>) -> None

def fetch_invites(self: Any) -> <class 'inspect._empty'>

def fetch_member(self: Any, member_id: <class 'str'>) -> <class 'EpikCord.ThreadMember'>

def fetch_message(self: Any, message_id: <class 'str'>) -> <class 'EpikCord.Message'>

def fetch_messages(self: Any, around: typing.Optional[str], before: typing.Optional[str], after: typing.Optional[str], limit: typing.Optional[int]) -> typing.List[EpikCord.Message]

def fetch_pinned_messages(self: Any) -> typing.List[EpikCord.Message]

def follow(self: Any, webhook_channel_id: <class 'str'>) -> <class 'inspect._empty'>

def join(self: Any) -> <class 'inspect._empty'>

def leave(self: Any) -> <class 'inspect._empty'>

def list_joined_private_archived_threads(self: Any, before: typing.Optional[str], limit: typing.Optional[int]) -> typing.Dict[str, typing.Union[typing.List[EpikCord.Messageable], typing.List[EpikCord.ThreadMember], bool]]

def list_members(self: Any) -> typing.List[EpikCord.ThreadMember]

def list_private_archived_threads(self: Any, before: typing.Optional[str], limit: typing.Optional[int]) -> typing.Dict[str, typing.Union[typing.List[EpikCord.Messageable], typing.List[EpikCord.ThreadMember], bool]]

def list_public_archived_threads(self: Any, before: typing.Optional[str], limit: typing.Optional[int]) -> typing.Dict[str, typing.Union[typing.List[EpikCord.Messageable], typing.List[EpikCord.ThreadMember], bool]]

def remove_member(self: Any, member_id: <class 'str'>) -> <class 'inspect._empty'>

def send(self: Any, content: typing.Optional[str], embeds: typing.Optional[typing.List[dict]], components: Any, tts: typing.Optional[bool], allowed_mentions: Any, sticker_ids: typing.Optional[typing.List[str]], attachments: typing.List[EpikCord.File], suppress_embeds: <class 'bool'>) -> <class 'EpikCord.Message'>

def start_thread(self: Any, name: <class 'str'>, auto_archive_duration: typing.Optional[int], type: typing.Optional[int], invitable: typing.Optional[bool], rate_limit_per_user: typing.Optional[int], reason: typing.Optional[str]) -> <class 'inspect._empty'>


GuildPreview
------------


GuildScheduledEvent
-------------------


GuildStageChannel
-----------------


GuildTextChannel
----------------

def bulk_delete(self: Any, message_ids: typing.List[str], reason: typing.Optional[str]) -> None

def create_invite(self: Any, max_age: typing.Optional[int], max_uses: typing.Optional[int], temporary: typing.Optional[bool], unique: typing.Optional[bool], target_type: typing.Optional[int], target_user_id: typing.Optional[str], target_application_id: typing.Optional[str]) -> <class 'inspect._empty'>

def create_webhook(self: Any, name: <class 'str'>, avatar: typing.Optional[str], reason: typing.Optional[str]) -> <class 'inspect._empty'>

def delete(self: Any, reason: typing.Optional[str]) -> None

def delete_overwrite(self: Any, overwrites: <class 'EpikCord.Overwrite'>) -> None

def fetch_invites(self: Any) -> <class 'inspect._empty'>

def fetch_message(self: Any, message_id: <class 'str'>) -> <class 'EpikCord.Message'>

def fetch_messages(self: Any, around: typing.Optional[str], before: typing.Optional[str], after: typing.Optional[str], limit: typing.Optional[int]) -> typing.List[EpikCord.Message]

def fetch_pinned_messages(self: Any) -> typing.List[EpikCord.Message]

def list_joined_private_archived_threads(self: Any, before: typing.Optional[str], limit: typing.Optional[int]) -> typing.Dict[str, typing.Union[typing.List[EpikCord.Messageable], typing.List[EpikCord.ThreadMember], bool]]

def list_private_archived_threads(self: Any, before: typing.Optional[str], limit: typing.Optional[int]) -> typing.Dict[str, typing.Union[typing.List[EpikCord.Messageable], typing.List[EpikCord.ThreadMember], bool]]

def list_public_archived_threads(self: Any, before: typing.Optional[str], limit: typing.Optional[int]) -> typing.Dict[str, typing.Union[typing.List[EpikCord.Messageable], typing.List[EpikCord.ThreadMember], bool]]

def send(self: Any, content: typing.Optional[str], embeds: typing.Optional[typing.List[dict]], components: Any, tts: typing.Optional[bool], allowed_mentions: Any, sticker_ids: typing.Optional[typing.List[str]], attachments: typing.List[EpikCord.File], suppress_embeds: <class 'bool'>) -> <class 'EpikCord.Message'>

def start_thread(self: Any, name: <class 'str'>, auto_archive_duration: typing.Optional[int], type: typing.Optional[int], invitable: typing.Optional[bool], rate_limit_per_user: typing.Optional[int], reason: typing.Optional[str]) -> <class 'inspect._empty'>


GuildWidget
-----------


GuildWidgetSettings
-------------------


HTTPClient
----------

def close(self: Any) -> NoneClose underlying connector.

Release all acquired resources.


def delete(self: Any, url: Any, args: Any, to_discord: <class 'bool'>, kwargs: Any) -> <class 'inspect._empty'>Perform HTTP DELETE request.


def detach(self: Any) -> NoneDetach connector from session without closing the former.

Session is switched to closed state anyway.


def get(self: Any, url: Any, args: Any, to_discord: <class 'bool'>, kwargs: Any) -> <class 'inspect._empty'>Perform HTTP GET request.


def head(self: Any, url: Any, args: Any, to_discord: <class 'bool'>, kwargs: Any) -> <class 'inspect._empty'>Perform HTTP HEAD request.


def log_request(self: Any, res: Any) -> <class 'inspect._empty'>

def options(self: Any, url: typing.Union[str, yarl.URL], allow_redirects: <class 'bool'>, kwargs: typing.Any) -> _RequestContextManagerPerform HTTP OPTIONS request.


def patch(self: Any, url: Any, args: Any, to_discord: <class 'bool'>, kwargs: Any) -> <class 'inspect._empty'>Perform HTTP PATCH request.


def post(self: Any, url: Any, args: Any, to_discord: <class 'bool'>, kwargs: Any) -> <class 'inspect._empty'>Perform HTTP POST request.


def put(self: Any, url: Any, args: Any, to_discord: <class 'bool'>, kwargs: Any) -> <class 'inspect._empty'>Perform HTTP PUT request.


def request(self: Any, method: <class 'str'>, url: typing.Union[str, yarl.URL], kwargs: typing.Any) -> _RequestContextManagerPerform HTTP request.


def ws_connect(self: Any, url: typing.Union[str, yarl.URL], method: <class 'str'>, protocols: typing.Iterable[str], timeout: <class 'float'>, receive_timeout: typing.Optional[float], autoclose: <class 'bool'>, autoping: <class 'bool'>, heartbeat: typing.Optional[float], auth: typing.Optional[aiohttp.helpers.BasicAuth], origin: typing.Optional[str], params: typing.Optional[typing.Mapping[str, str]], headers: typing.Union[typing.Mapping[typing.Union[str, multidict._multidict.istr], str], multidict._multidict.CIMultiDict, multidict._multidict.CIMultiDictProxy, NoneType], proxy: typing.Union[str, yarl.URL, NoneType], proxy_auth: typing.Optional[aiohttp.helpers.BasicAuth], ssl: typing.Union[ssl.SSLContext, bool, NoneType, aiohttp.client_reqrep.Fingerprint], verify_ssl: typing.Optional[bool], fingerprint: typing.Optional[bytes], ssl_context: typing.Optional[ssl.SSLContext], proxy_headers: typing.Union[typing.Mapping[typing.Union[str, multidict._multidict.istr], str], multidict._multidict.CIMultiDict, multidict._multidict.CIMultiDictProxy, NoneType], compress: <class 'int'>, max_msg_size: <class 'int'>) -> _WSRequestContextManagerInitiate websocket connection.



IntegerOption
-------------

def to_dict(self: Any) -> <class 'inspect._empty'>


Integration
-----------


IntegrationAccount
------------------


Intents
-------

def calculate_from_turned(self: Any) -> <class 'inspect._empty'>


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

def to_dict(self: Any) -> <class 'inspect._empty'>


MentionedChannel
----------------


MentionedUser
-------------

def fetch_message(self: Any, message_id: <class 'str'>) -> <class 'EpikCord.Message'>

def fetch_messages(self: Any, around: typing.Optional[str], before: typing.Optional[str], after: typing.Optional[str], limit: typing.Optional[int]) -> typing.List[EpikCord.Message]

def send(self: Any, content: typing.Optional[str], embeds: typing.Optional[typing.List[dict]], components: Any, tts: typing.Optional[bool], allowed_mentions: Any, sticker_ids: typing.Optional[typing.List[str]], attachments: typing.List[EpikCord.File], suppress_embeds: <class 'bool'>) -> <class 'EpikCord.Message'>


Message
-------

def add_reaction(self: Any, emoji: <class 'str'>) -> <class 'inspect._empty'>

def crosspost(self: Any) -> <class 'inspect._empty'>

def delete(self: Any) -> <class 'inspect._empty'>

def delete_all_reactions(self: Any) -> <class 'inspect._empty'>

def delete_reaction_for_emoji(self: Any, emoji: <class 'str'>) -> <class 'inspect._empty'>

def edit(self: Any, message_data: <class 'dict'>) -> <class 'inspect._empty'>

def fetch_reactions(self: Any, after: Any, limit: Any) -> typing.List[EpikCord.Reaction]

def pin(self: Any, reason: typing.Optional[str]) -> <class 'inspect._empty'>

def remove_reaction(self: Any, emoji: <class 'str'>, user: Any) -> <class 'inspect._empty'>

def start_thread(self: Any, name: <class 'str'>, auto_archive_duration: typing.Optional[int], rate_limit_per_user: typing.Optional[int]) -> <class 'inspect._empty'>

def unpin(self: Any, reason: typing.Optional[str]) -> <class 'inspect._empty'>


MessageActivity
---------------


MessageCommandInteraction
-------------------------

def create_followup(self: Any, tts: <class 'bool'>, content: typing.Optional[str], embeds: typing.Optional[typing.List[EpikCord.Embed]], allowed_mentions: Any, components: typing.Optional[typing.List[typing.Union[EpikCord.components.Button, EpikCord.components.SelectMenu, EpikCord.components.TextInput]]], attachments: typing.Optional[typing.List[EpikCord.Attachment]], suppress_embeds: typing.Optional[bool], ephemeral: typing.Optional[bool]) -> None

def defer(self: Any, show_loading_state: typing.Optional[bool]) -> <class 'inspect._empty'>

def delete_followup(self: Any) -> <class 'inspect._empty'>

def delete_original_response(self: Any) -> <class 'inspect._empty'>

def edit_followup(self: Any, tts: <class 'bool'>, content: typing.Optional[str], embeds: typing.Optional[typing.List[EpikCord.Embed]], allowed_mentions: Any, components: typing.Optional[typing.List[typing.Union[EpikCord.components.Button, EpikCord.components.SelectMenu, EpikCord.components.TextInput]]], attachments: typing.Optional[typing.List[EpikCord.Attachment]], suppress_embeds: typing.Optional[bool], ephemeral: typing.Optional[bool]) -> None

def edit_original_response(self: Any, tts: <class 'bool'>, content: typing.Optional[str], embeds: typing.Optional[typing.List[EpikCord.Embed]], allowed_mentions: Any, components: typing.Optional[typing.List[typing.Union[EpikCord.components.Button, EpikCord.components.SelectMenu, EpikCord.components.TextInput]]], attachments: typing.Optional[typing.List[EpikCord.Attachment]], suppress_embeds: typing.Optional[bool], ephemeral: typing.Optional[bool]) -> None

def fetch_original_response(self: Any, skip_cache: typing.Optional[bool]) -> <class 'inspect._empty'>

def is_application_command(self: Any) -> <class 'inspect._empty'>

def is_autocomplete(self: Any) -> <class 'inspect._empty'>

def is_message_component(self: Any) -> <class 'inspect._empty'>

def is_modal_submit(self: Any) -> <class 'inspect._empty'>

def is_ping(self: Any) -> <class 'inspect._empty'>

def reply(self: Any, tts: <class 'bool'>, content: typing.Optional[str], embeds: typing.Optional[typing.List[EpikCord.Embed]], allowed_mentions: Any, components: typing.Optional[typing.List[typing.Union[EpikCord.components.Button, EpikCord.components.SelectMenu, EpikCord.components.TextInput]]], attachments: typing.Optional[typing.List[EpikCord.Attachment]], suppress_embeds: typing.Optional[bool], ephemeral: typing.Optional[bool]) -> None

def send_modal(self: Any, modal: <class 'EpikCord.Modal'>) -> <class 'inspect._empty'>


MessageComponentInteraction
---------------------------

def create_followup(self: Any, tts: <class 'bool'>, content: typing.Optional[str], embeds: typing.Optional[typing.List[EpikCord.Embed]], allowed_mentions: Any, components: typing.Optional[typing.List[typing.Union[EpikCord.components.Button, EpikCord.components.SelectMenu, EpikCord.components.TextInput]]], attachments: typing.Optional[typing.List[EpikCord.Attachment]], suppress_embeds: typing.Optional[bool], ephemeral: typing.Optional[bool]) -> None

def defer(self: Any, show_loading_state: typing.Optional[bool]) -> <class 'inspect._empty'>

def defer_update(self: Any) -> <class 'inspect._empty'>

def delete_followup(self: Any) -> <class 'inspect._empty'>

def delete_original_response(self: Any) -> <class 'inspect._empty'>

def edit_followup(self: Any, tts: <class 'bool'>, content: typing.Optional[str], embeds: typing.Optional[typing.List[EpikCord.Embed]], allowed_mentions: Any, components: typing.Optional[typing.List[typing.Union[EpikCord.components.Button, EpikCord.components.SelectMenu, EpikCord.components.TextInput]]], attachments: typing.Optional[typing.List[EpikCord.Attachment]], suppress_embeds: typing.Optional[bool], ephemeral: typing.Optional[bool]) -> None

def edit_original_response(self: Any, tts: <class 'bool'>, content: typing.Optional[str], embeds: typing.Optional[typing.List[EpikCord.Embed]], allowed_mentions: Any, components: typing.Optional[typing.List[typing.Union[EpikCord.components.Button, EpikCord.components.SelectMenu, EpikCord.components.TextInput]]], attachments: typing.Optional[typing.List[EpikCord.Attachment]], suppress_embeds: typing.Optional[bool], ephemeral: typing.Optional[bool]) -> None

def fetch_original_response(self: Any, skip_cache: typing.Optional[bool]) -> <class 'inspect._empty'>

def is_action_row(self: Any) -> <class 'inspect._empty'>

def is_application_command(self: Any) -> <class 'inspect._empty'>

def is_autocomplete(self: Any) -> <class 'inspect._empty'>

def is_button(self: Any) -> <class 'inspect._empty'>

def is_message_component(self: Any) -> <class 'inspect._empty'>

def is_modal_submit(self: Any) -> <class 'inspect._empty'>

def is_ping(self: Any) -> <class 'inspect._empty'>

def is_select_menu(self: Any) -> <class 'inspect._empty'>

def is_text_input(self: Any) -> <class 'inspect._empty'>

def reply(self: Any, tts: <class 'bool'>, content: typing.Optional[str], embeds: typing.Optional[typing.List[EpikCord.Embed]], allowed_mentions: Any, components: typing.Optional[typing.List[typing.Union[EpikCord.components.Button, EpikCord.components.SelectMenu, EpikCord.components.TextInput]]], attachments: typing.Optional[typing.List[EpikCord.Attachment]], suppress_embeds: typing.Optional[bool], ephemeral: typing.Optional[bool]) -> None

def send_modal(self: Any, modal: <class 'EpikCord.Modal'>) -> <class 'inspect._empty'>

def update(self: Any, tts: <class 'bool'>, content: typing.Optional[str], embeds: typing.Optional[typing.List[EpikCord.Embed]], allowed_mentions: Any, components: typing.Optional[typing.List[typing.Union[EpikCord.components.Button, EpikCord.components.SelectMenu, EpikCord.components.TextInput]]], attachments: typing.Optional[typing.List[EpikCord.Attachment]], suppress_embeds: typing.Optional[bool]) -> None


MessageInteraction
------------------


Messageable
-----------

def fetch_message(self: Any, message_id: <class 'str'>) -> <class 'EpikCord.Message'>

def fetch_messages(self: Any, around: typing.Optional[str], before: typing.Optional[str], after: typing.Optional[str], limit: typing.Optional[int]) -> typing.List[EpikCord.Message]

def send(self: Any, content: typing.Optional[str], embeds: typing.Optional[typing.List[dict]], components: Any, tts: typing.Optional[bool], allowed_mentions: Any, sticker_ids: typing.Optional[typing.List[str]], attachments: typing.List[EpikCord.File], suppress_embeds: <class 'bool'>) -> <class 'EpikCord.Message'>


MethodNotAllowed405
-------------------


MissingClientSetting
--------------------


MissingCustomId
---------------


Modal
-----

def to_dict(self: Any) -> <class 'inspect._empty'>


ModalSubmitInteraction
----------------------

def create_followup(self: Any, tts: <class 'bool'>, content: typing.Optional[str], embeds: typing.Optional[typing.List[EpikCord.Embed]], allowed_mentions: Any, components: typing.Optional[typing.List[typing.Union[EpikCord.components.Button, EpikCord.components.SelectMenu, EpikCord.components.TextInput]]], attachments: typing.Optional[typing.List[EpikCord.Attachment]], suppress_embeds: typing.Optional[bool], ephemeral: typing.Optional[bool]) -> None

def defer(self: Any, show_loading_state: typing.Optional[bool]) -> <class 'inspect._empty'>

def delete_followup(self: Any) -> <class 'inspect._empty'>

def delete_original_response(self: Any) -> <class 'inspect._empty'>

def edit_followup(self: Any, tts: <class 'bool'>, content: typing.Optional[str], embeds: typing.Optional[typing.List[EpikCord.Embed]], allowed_mentions: Any, components: typing.Optional[typing.List[typing.Union[EpikCord.components.Button, EpikCord.components.SelectMenu, EpikCord.components.TextInput]]], attachments: typing.Optional[typing.List[EpikCord.Attachment]], suppress_embeds: typing.Optional[bool], ephemeral: typing.Optional[bool]) -> None

def edit_original_response(self: Any, tts: <class 'bool'>, content: typing.Optional[str], embeds: typing.Optional[typing.List[EpikCord.Embed]], allowed_mentions: Any, components: typing.Optional[typing.List[typing.Union[EpikCord.components.Button, EpikCord.components.SelectMenu, EpikCord.components.TextInput]]], attachments: typing.Optional[typing.List[EpikCord.Attachment]], suppress_embeds: typing.Optional[bool], ephemeral: typing.Optional[bool]) -> None

def fetch_original_response(self: Any, skip_cache: typing.Optional[bool]) -> <class 'inspect._empty'>

def is_application_command(self: Any) -> <class 'inspect._empty'>

def is_autocomplete(self: Any) -> <class 'inspect._empty'>

def is_message_component(self: Any) -> <class 'inspect._empty'>

def is_modal_submit(self: Any) -> <class 'inspect._empty'>

def is_ping(self: Any) -> <class 'inspect._empty'>

def reply(self: Any, tts: <class 'bool'>, content: typing.Optional[str], embeds: typing.Optional[typing.List[EpikCord.Embed]], allowed_mentions: Any, components: typing.Optional[typing.List[typing.Union[EpikCord.components.Button, EpikCord.components.SelectMenu, EpikCord.components.TextInput]]], attachments: typing.Optional[typing.List[EpikCord.Attachment]], suppress_embeds: typing.Optional[bool], ephemeral: typing.Optional[bool]) -> None

def send_modal(self: Any, args: Any, kwargs: Any) -> <class 'inspect._empty'>


NotFound404
-----------


NumberOption
------------

def to_dict(self: Any) -> <class 'inspect._empty'>


Overwrite
---------


Paginator
---------

def add_page(self: Any, page: <class 'EpikCord.Embed'>) -> <class 'inspect._empty'>

def back(self: Any) -> <class 'inspect._empty'>

def current(self: Any) -> <class 'EpikCord.Embed'>

def forward(self: Any) -> <class 'inspect._empty'>

def remove_page(self: Any, page: <class 'EpikCord.Embed'>) -> <class 'inspect._empty'>


PartialEmoji
------------

def to_dict(self: Any) -> <class 'inspect._empty'>


PartialGuild
------------


PartialUser
-----------


Permissions
-----------

def calculate_from_turned(self: Any) -> <class 'inspect._empty'>


Presence
--------

def to_dict(self: Any) -> <class 'inspect._empty'>


PrivateThread
-------------

def add_member(self: Any, member_id: <class 'str'>) -> <class 'inspect._empty'>

def bulk_delete(self: Any, message_ids: typing.List[str], reason: typing.Optional[str]) -> None

def fetch_member(self: Any, member_id: <class 'str'>) -> <class 'EpikCord.ThreadMember'>

def join(self: Any) -> <class 'inspect._empty'>

def leave(self: Any) -> <class 'inspect._empty'>

def list_members(self: Any) -> typing.List[EpikCord.ThreadMember]

def remove_member(self: Any, member_id: <class 'str'>) -> <class 'inspect._empty'>


RatelimitHandler
----------------

def is_ratelimited(self: Any) -> <class 'bool'>Checks if the client is ratelimited.


def process_headers(self: Any, headers: <class 'dict'>) -> <class 'inspect._empty'>Read the headers from a request and then digest it.



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

def to_dict(self: Any) -> <class 'inspect._empty'>


RoleTag
-------


SelectMenu
----------

def add_options(self: Any, options: typing.List[EpikCord.components.SelectMenuOption]) -> <class 'inspect._empty'>

def set_custom_id(self: Any, custom_id: <class 'str'>) -> <class 'inspect._empty'>

def set_disabled(self: Any, disabled: <class 'bool'>) -> <class 'inspect._empty'>

def set_max_values(self: Any, max: <class 'int'>) -> <class 'inspect._empty'>

def set_min_values(self: Any, min: <class 'int'>) -> <class 'inspect._empty'>

def set_placeholder(self: Any, placeholder: <class 'str'>) -> <class 'inspect._empty'>

def to_dict(self: Any) -> <class 'inspect._empty'>


SelectMenuOption
----------------

def to_dict(self: Any) -> <class 'inspect._empty'>


Shard
-----

def change_presence(self: Any, presence: typing.Optional[EpikCord.Presence]) -> <class 'inspect._empty'>

def channel_create(self: Any, data: <class 'dict'>) -> <class 'inspect._empty'>

def close(self: Any) -> None

def component(self: Any, custom_id: <class 'str'>) -> <class 'inspect._empty'>Execute this function when a component with the `custom_id` is interacted with.


def connect(self: Any) -> <class 'inspect._empty'>

def event(self: Any, func: Any) -> <class 'inspect._empty'>

def get_event_callback(self: Any, event_name: <class 'str'>, internal: Any) -> <class 'inspect._empty'>

def guild_create(self: Any, data: Any) -> <class 'inspect._empty'>

def guild_delete(self: Any, data: <class 'dict'>) -> <class 'inspect._empty'>

def guild_member_update(self: Any, data: Any) -> <class 'inspect._empty'>

def guild_members_chunk(self: Any, data: <class 'dict'>) -> <class 'inspect._empty'>

def handle_close(self: Any) -> <class 'inspect._empty'>

def handle_event(self: Any, event_name: typing.Optional[str], data: <class 'dict'>) -> <class 'inspect._empty'>

def handle_events(self: Any) -> <class 'inspect._empty'>

def heartbeat(self: Any, forced: typing.Optional[bool]) -> <class 'inspect._empty'>

def identify(self: Any) -> <class 'inspect._empty'>

def interaction_create(self: Any, data: Any) -> <class 'inspect._empty'>

def login(self: Any) -> <class 'inspect._empty'>

def message_create(self: Any, data: <class 'dict'>) -> <class 'inspect._empty'>Event fired when messages are created


def ready(self: Any, data: <class 'dict'>) -> <class 'inspect._empty'>

def reconnect(self: Any) -> <class 'inspect._empty'>

def request_guild_members(self: Any, guild_id: <class 'int'>, query: typing.Optional[str], limit: typing.Optional[int], presences: typing.Optional[bool], user_ids: typing.Optional[typing.List[str]], nonce: typing.Optional[str]) -> <class 'inspect._empty'>

def resume(self: Any) -> <class 'inspect._empty'>

def send_json(self: Any, json: <class 'dict'>) -> <class 'inspect._empty'>

def voice_server_update(self: Any, data: <class 'dict'>) -> <class 'inspect._empty'>

def wait_for(self: Any, event_name: <class 'str'>, check: typing.Optional[<built-in function callable>], timeout: typing.Union[float, int, NoneType]) -> <class 'inspect._empty'>


ShardingRequired
----------------


SlashCommand
------------

def to_dict(self: Any) -> <class 'inspect._empty'>


SlashCommandOptionChoice
------------------------

def to_dict(self: Any) -> <class 'inspect._empty'>


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

def to_dict(self: Any) -> <class 'inspect._empty'>


SubCommandGroup
---------------

def to_dict(self: Any) -> <class 'inspect._empty'>


Subcommand
----------

def to_dict(self: Any) -> <class 'inspect._empty'>


SystemChannelFlags
------------------


Team
----


TeamMember
----------


TextInput
---------

def set_custom_id(self: Any, custom_id: <class 'str'>) -> <class 'inspect._empty'>

def to_dict(self: Any) -> <class 'inspect._empty'>


Thread
------

def add_member(self: Any, member_id: <class 'str'>) -> <class 'inspect._empty'>

def bulk_delete(self: Any, message_ids: typing.List[str], reason: typing.Optional[str]) -> None

def fetch_member(self: Any, member_id: <class 'str'>) -> <class 'EpikCord.ThreadMember'>

def join(self: Any) -> <class 'inspect._empty'>

def leave(self: Any) -> <class 'inspect._empty'>

def list_members(self: Any) -> typing.List[EpikCord.ThreadMember]

def remove_member(self: Any, member_id: <class 'str'>) -> <class 'inspect._empty'>


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

def fetch_message(self: Any, message_id: <class 'str'>) -> <class 'EpikCord.Message'>

def fetch_messages(self: Any, around: typing.Optional[str], before: typing.Optional[str], after: typing.Optional[str], limit: typing.Optional[int]) -> typing.List[EpikCord.Message]

def send(self: Any, content: typing.Optional[str], embeds: typing.Optional[typing.List[dict]], components: Any, tts: typing.Optional[bool], allowed_mentions: Any, sticker_ids: typing.Optional[typing.List[str]], attachments: typing.List[EpikCord.File], suppress_embeds: <class 'bool'>) -> <class 'EpikCord.Message'>


UserCommandInteraction
----------------------

def create_followup(self: Any, tts: <class 'bool'>, content: typing.Optional[str], embeds: typing.Optional[typing.List[EpikCord.Embed]], allowed_mentions: Any, components: typing.Optional[typing.List[typing.Union[EpikCord.components.Button, EpikCord.components.SelectMenu, EpikCord.components.TextInput]]], attachments: typing.Optional[typing.List[EpikCord.Attachment]], suppress_embeds: typing.Optional[bool], ephemeral: typing.Optional[bool]) -> None

def defer(self: Any, show_loading_state: typing.Optional[bool]) -> <class 'inspect._empty'>

def delete_followup(self: Any) -> <class 'inspect._empty'>

def delete_original_response(self: Any) -> <class 'inspect._empty'>

def edit_followup(self: Any, tts: <class 'bool'>, content: typing.Optional[str], embeds: typing.Optional[typing.List[EpikCord.Embed]], allowed_mentions: Any, components: typing.Optional[typing.List[typing.Union[EpikCord.components.Button, EpikCord.components.SelectMenu, EpikCord.components.TextInput]]], attachments: typing.Optional[typing.List[EpikCord.Attachment]], suppress_embeds: typing.Optional[bool], ephemeral: typing.Optional[bool]) -> None

def edit_original_response(self: Any, tts: <class 'bool'>, content: typing.Optional[str], embeds: typing.Optional[typing.List[EpikCord.Embed]], allowed_mentions: Any, components: typing.Optional[typing.List[typing.Union[EpikCord.components.Button, EpikCord.components.SelectMenu, EpikCord.components.TextInput]]], attachments: typing.Optional[typing.List[EpikCord.Attachment]], suppress_embeds: typing.Optional[bool], ephemeral: typing.Optional[bool]) -> None

def fetch_original_response(self: Any, skip_cache: typing.Optional[bool]) -> <class 'inspect._empty'>

def is_application_command(self: Any) -> <class 'inspect._empty'>

def is_autocomplete(self: Any) -> <class 'inspect._empty'>

def is_message_component(self: Any) -> <class 'inspect._empty'>

def is_modal_submit(self: Any) -> <class 'inspect._empty'>

def is_ping(self: Any) -> <class 'inspect._empty'>

def reply(self: Any, tts: <class 'bool'>, content: typing.Optional[str], embeds: typing.Optional[typing.List[EpikCord.Embed]], allowed_mentions: Any, components: typing.Optional[typing.List[typing.Union[EpikCord.components.Button, EpikCord.components.SelectMenu, EpikCord.components.TextInput]]], attachments: typing.Optional[typing.List[EpikCord.Attachment]], suppress_embeds: typing.Optional[bool], ephemeral: typing.Optional[bool]) -> None

def send_modal(self: Any, modal: <class 'EpikCord.Modal'>) -> <class 'inspect._empty'>


UserOption
----------

def to_dict(self: Any) -> <class 'inspect._empty'>


Utils
-----

def cancel_tasks(self: Any, loop: Any) -> None

def channel_from_type(self: Any, channel_data: <class 'dict'>) -> <class 'inspect._empty'>

def cleanup_loop(self: Any, loop: Any) -> None

def component_from_type(self: Any, component_data: <class 'dict'>) -> <class 'inspect._empty'>

def compute_timedelta(self: Any, dt: <class 'datetime.datetime'>) -> <class 'inspect._empty'>

def escape_markdown(self: Any, text: <class 'str'>, as_needed: <class 'bool'>, ignore_links: <class 'bool'>) -> <class 'str'>

def escape_mentions(self: Any, text: <class 'str'>) -> <class 'str'>

def get_mime_type_for_image(self: Any, data: <class 'bytes'>) -> <class 'inspect._empty'>

def interaction_from_type(self: Any, data: Any) -> <class 'inspect._empty'>

def remove_markdown(self: Any, text: <class 'str'>, ignore_links: <class 'bool'>) -> <class 'str'>

def sleep_until(self: Any, when: typing.Union[datetime.datetime, int, float], result: typing.Optional[~T]) -> typing.Optional[~T]

def utcnow(self: Any) -> <class 'datetime.datetime'>


VoiceChannel
------------

def create_invite(self: Any, max_age: typing.Optional[int], max_uses: typing.Optional[int], temporary: typing.Optional[bool], unique: typing.Optional[bool], target_type: typing.Optional[int], target_user_id: typing.Optional[str], target_application_id: typing.Optional[str]) -> <class 'inspect._empty'>

def delete(self: Any, reason: typing.Optional[str]) -> None

def delete_overwrite(self: Any, overwrites: <class 'EpikCord.Overwrite'>) -> None

def fetch_invites(self: Any) -> <class 'inspect._empty'>

def fetch_pinned_messages(self: Any) -> typing.List[EpikCord.Message]


VoiceState
----------


VoiceWebsocketClient
--------------------

def connect(self: Any, muted: typing.Optional[bool], deafened: typing.Optional[bool]) -> <class 'inspect._empty'>


Webhook
-------


WebhookUser
-----------


WebsocketClient
---------------

def change_presence(self: Any, presence: typing.Optional[EpikCord.Presence]) -> <class 'inspect._empty'>

def channel_create(self: Any, data: <class 'dict'>) -> <class 'inspect._empty'>

def close(self: Any) -> None

def component(self: Any, custom_id: <class 'str'>) -> <class 'inspect._empty'>Execute this function when a component with the `custom_id` is interacted with.


def connect(self: Any) -> <class 'inspect._empty'>

def event(self: Any, func: Any) -> <class 'inspect._empty'>

def get_event_callback(self: Any, event_name: <class 'str'>, internal: Any) -> <class 'inspect._empty'>

def guild_create(self: Any, data: Any) -> <class 'inspect._empty'>

def guild_delete(self: Any, data: <class 'dict'>) -> <class 'inspect._empty'>

def guild_member_update(self: Any, data: Any) -> <class 'inspect._empty'>

def guild_members_chunk(self: Any, data: <class 'dict'>) -> <class 'inspect._empty'>

def handle_close(self: Any) -> <class 'inspect._empty'>

def handle_event(self: Any, event_name: typing.Optional[str], data: <class 'dict'>) -> <class 'inspect._empty'>

def handle_events(self: Any) -> <class 'inspect._empty'>

def heartbeat(self: Any, forced: typing.Optional[bool]) -> <class 'inspect._empty'>

def identify(self: Any) -> <class 'inspect._empty'>

def interaction_create(self: Any, data: Any) -> <class 'inspect._empty'>

def login(self: Any) -> <class 'inspect._empty'>

def message_create(self: Any, data: <class 'dict'>) -> <class 'inspect._empty'>Event fired when messages are created


def ready(self: Any, data: <class 'dict'>) -> <class 'inspect._empty'>

def reconnect(self: Any) -> <class 'inspect._empty'>

def request_guild_members(self: Any, guild_id: <class 'int'>, query: typing.Optional[str], limit: typing.Optional[int], presences: typing.Optional[bool], user_ids: typing.Optional[typing.List[str]], nonce: typing.Optional[str]) -> <class 'inspect._empty'>

def resume(self: Any) -> <class 'inspect._empty'>

def send_json(self: Any, json: <class 'dict'>) -> <class 'inspect._empty'>

def voice_server_update(self: Any, data: <class 'dict'>) -> <class 'inspect._empty'>

def wait_for(self: Any, event_name: <class 'str'>, check: typing.Optional[<built-in function callable>], timeout: typing.Union[float, int, NoneType]) -> <class 'inspect._empty'>


WelcomeScreen
-------------


WelcomeScreenChannel
--------------------
