

ActionRow
---------

def add_components(self: Any, components: typing.List[typing.Union[EpikCord.components.Button, EpikCord.components.SelectMenu]])

def to_dict(self: Any)


Activity
--------

def to_dict(self: Any)Returns activity class as dict

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

def create_followup(self: Any, tts: <class 'bool'>, content: typing.Optional[str], embeds: typing.Optional[typing.List[EpikCord.Embed]], allowed_mentions: Any, components: typing.Optional[typing.List[typing.Union[EpikCord.components.Button, EpikCord.components.SelectMenu, EpikCord.components.TextInput]]], attachments: typing.Optional[typing.List[EpikCord.Attachment]], suppress_embeds: typing.Optional[bool], ephemeral: typing.Optional[bool])

def defer(self: Any, show_loading_state: typing.Optional[bool])

def delete_followup(self: Any)

def delete_original_response(self: Any)

def edit_followup(self: Any, tts: <class 'bool'>, content: typing.Optional[str], embeds: typing.Optional[typing.List[EpikCord.Embed]], allowed_mentions: Any, components: typing.Optional[typing.List[typing.Union[EpikCord.components.Button, EpikCord.components.SelectMenu, EpikCord.components.TextInput]]], attachments: typing.Optional[typing.List[EpikCord.Attachment]], suppress_embeds: typing.Optional[bool], ephemeral: typing.Optional[bool])

def edit_original_response(self: Any, tts: <class 'bool'>, content: typing.Optional[str], embeds: typing.Optional[typing.List[EpikCord.Embed]], allowed_mentions: Any, components: typing.Optional[typing.List[typing.Union[EpikCord.components.Button, EpikCord.components.SelectMenu, EpikCord.components.TextInput]]], attachments: typing.Optional[typing.List[EpikCord.Attachment]], suppress_embeds: typing.Optional[bool], ephemeral: typing.Optional[bool])

def fetch_original_response(self: Any, skip_cache: typing.Optional[bool])

def is_application_command(self: Any)

def is_autocomplete(self: Any)

def is_message_component(self: Any)

def is_modal_submit(self: Any)

def is_ping(self: Any)

def reply(self: Any, tts: <class 'bool'>, content: typing.Optional[str], embeds: typing.Optional[typing.List[EpikCord.Embed]], allowed_mentions: Any, components: typing.Optional[typing.List[typing.Union[EpikCord.components.Button, EpikCord.components.SelectMenu, EpikCord.components.TextInput]]], attachments: typing.Optional[typing.List[EpikCord.Attachment]], suppress_embeds: typing.Optional[bool], ephemeral: typing.Optional[bool])

def send_modal(self: Any, modal: <class 'EpikCord.Modal'>)


ApplicationCommandOption
------------------------


ApplicationCommandPermission
----------------------------

def to_dict(self: Any)


ApplicationCommandSubcommandOption
----------------------------------


Attachment
----------


AttachmentOption
----------------

def to_dict(self: Any)


AutoCompleteInteraction
-----------------------

def create_followup(self: Any, tts: <class 'bool'>, content: typing.Optional[str], embeds: typing.Optional[typing.List[EpikCord.Embed]], allowed_mentions: Any, components: typing.Optional[typing.List[typing.Union[EpikCord.components.Button, EpikCord.components.SelectMenu, EpikCord.components.TextInput]]], attachments: typing.Optional[typing.List[EpikCord.Attachment]], suppress_embeds: typing.Optional[bool], ephemeral: typing.Optional[bool])

def defer(self: Any, show_loading_state: typing.Optional[bool])

def delete_followup(self: Any)

def delete_original_response(self: Any)

def edit_followup(self: Any, tts: <class 'bool'>, content: typing.Optional[str], embeds: typing.Optional[typing.List[EpikCord.Embed]], allowed_mentions: Any, components: typing.Optional[typing.List[typing.Union[EpikCord.components.Button, EpikCord.components.SelectMenu, EpikCord.components.TextInput]]], attachments: typing.Optional[typing.List[EpikCord.Attachment]], suppress_embeds: typing.Optional[bool], ephemeral: typing.Optional[bool])

def edit_original_response(self: Any, tts: <class 'bool'>, content: typing.Optional[str], embeds: typing.Optional[typing.List[EpikCord.Embed]], allowed_mentions: Any, components: typing.Optional[typing.List[typing.Union[EpikCord.components.Button, EpikCord.components.SelectMenu, EpikCord.components.TextInput]]], attachments: typing.Optional[typing.List[EpikCord.Attachment]], suppress_embeds: typing.Optional[bool], ephemeral: typing.Optional[bool])

def fetch_original_response(self: Any, skip_cache: typing.Optional[bool])

def is_application_command(self: Any)

def is_autocomplete(self: Any)

def is_message_component(self: Any)

def is_modal_submit(self: Any)

def is_ping(self: Any)

def reply(self: Any, choices: typing.List[EpikCord.options.SlashCommandOptionChoice])

def send_modal(self: Any, modal: <class 'EpikCord.Modal'>)


BadRequest400
-------------


BaseChannel
-----------


BaseComponent
-------------

def set_custom_id(self: Any, custom_id: <class 'str'>)


BaseInteraction
---------------

def create_followup(self: Any, tts: <class 'bool'>, content: typing.Optional[str], embeds: typing.Optional[typing.List[EpikCord.Embed]], allowed_mentions: Any, components: typing.Optional[typing.List[typing.Union[EpikCord.components.Button, EpikCord.components.SelectMenu, EpikCord.components.TextInput]]], attachments: typing.Optional[typing.List[EpikCord.Attachment]], suppress_embeds: typing.Optional[bool], ephemeral: typing.Optional[bool])

def defer(self: Any, show_loading_state: typing.Optional[bool])

def delete_followup(self: Any)

def delete_original_response(self: Any)

def edit_followup(self: Any, tts: <class 'bool'>, content: typing.Optional[str], embeds: typing.Optional[typing.List[EpikCord.Embed]], allowed_mentions: Any, components: typing.Optional[typing.List[typing.Union[EpikCord.components.Button, EpikCord.components.SelectMenu, EpikCord.components.TextInput]]], attachments: typing.Optional[typing.List[EpikCord.Attachment]], suppress_embeds: typing.Optional[bool], ephemeral: typing.Optional[bool])

def edit_original_response(self: Any, tts: <class 'bool'>, content: typing.Optional[str], embeds: typing.Optional[typing.List[EpikCord.Embed]], allowed_mentions: Any, components: typing.Optional[typing.List[typing.Union[EpikCord.components.Button, EpikCord.components.SelectMenu, EpikCord.components.TextInput]]], attachments: typing.Optional[typing.List[EpikCord.Attachment]], suppress_embeds: typing.Optional[bool], ephemeral: typing.Optional[bool])

def fetch_original_response(self: Any, skip_cache: typing.Optional[bool])

def is_application_command(self: Any)

def is_autocomplete(self: Any)

def is_message_component(self: Any)

def is_modal_submit(self: Any)

def is_ping(self: Any)

def reply(self: Any, tts: <class 'bool'>, content: typing.Optional[str], embeds: typing.Optional[typing.List[EpikCord.Embed]], allowed_mentions: Any, components: typing.Optional[typing.List[typing.Union[EpikCord.components.Button, EpikCord.components.SelectMenu, EpikCord.components.TextInput]]], attachments: typing.Optional[typing.List[EpikCord.Attachment]], suppress_embeds: typing.Optional[bool], ephemeral: typing.Optional[bool])

def send_modal(self: Any, modal: <class 'EpikCord.Modal'>)


BaseSlashCommandOption
----------------------

def to_dict(self: Any)


BooleanOption
-------------

def to_dict(self: Any)


Button
------

def set_custom_id(self: Any, custom_id: <class 'str'>)

def set_emoji(self: Any, emoji: typing.Union[EpikCord.partials.PartialEmoji, dict])

def set_label(self: Any, label: <class 'str'>)

def set_style(self: Any, style: typing.Union[int, str])

def set_url(self: Any, url: <class 'str'>)

def to_dict(self: Any)


CacheManager
------------

def add_to_cache(self: Any, key: Any, value: Any)

def clear_cache(self: Any)

def get_from_cache(self: Any, key: Any)

def is_in_cache(self: Any, key: Any)

def remove_from_cache(self: Any, key: Any)


ChannelCategory
---------------

def create_invite(self: Any, max_age: typing.Optional[int], max_uses: typing.Optional[int], temporary: typing.Optional[bool], unique: typing.Optional[bool], target_type: typing.Optional[int], target_user_id: typing.Optional[str], target_application_id: typing.Optional[str])

def delete(self: Any, reason: typing.Optional[str])

def delete_overwrite(self: Any, overwrites: <class 'EpikCord.Overwrite'>)

def fetch_invites(self: Any)

def fetch_pinned_messages(self: Any)


ChannelManager
--------------

def add_to_cache(self: Any, key: Any, value: Any)

def clear_cache(self: Any)

def fetch(self: Any, channel_id: Any, skip_cache: typing.Optional[bool])

def format_cache(self: Any)

def get_from_cache(self: Any, key: Any)

def is_in_cache(self: Any, key: Any)

def remove_from_cache(self: Any, key: Any)


ChannelOption
-------------

def to_dict(self: Any)


ChannelOptionChannelTypes
-------------------------


Client
------

def add_section(self: Any, section: typing.Union[EpikCord.CommandsSection, EpikCord.EventsSection])

def change_presence(self: Any, presence: typing.Optional[EpikCord.Presence])

def channel_create(self: Any, data: <class 'dict'>)

def close(self: Any)

def command(self: Any, name: typing.Optional[str], description: typing.Optional[str], guild_ids: typing.Optional[typing.List[str]], options: typing.Union[EpikCord.options.Subcommand, EpikCord.options.SubCommandGroup, EpikCord.options.StringOption, EpikCord.options.IntegerOption, EpikCord.options.BooleanOption, EpikCord.options.UserOption, EpikCord.options.ChannelOption, EpikCord.options.RoleOption, EpikCord.options.MentionableOption, EpikCord.options.NumberOption, NoneType])

def component(self: Any, custom_id: <class 'str'>)
    Execute this function when a component with the `custom_id` is interacted with.
        


def connect(self: Any)

def event(self: Any, func: Any)

def get_event_callback(self: Any, event_name: <class 'str'>, internal: Any)

def guild_create(self: Any, data: Any)

def guild_delete(self: Any, data: <class 'dict'>)

def guild_member_update(self: Any, data: Any)

def guild_members_chunk(self: Any, data: <class 'dict'>)

def handle_close(self: Any)

def handle_event(self: Any, event_name: typing.Optional[str], data: <class 'dict'>)

def handle_events(self: Any)

def heartbeat(self: Any, forced: typing.Optional[bool])

def identify(self: Any)

def interaction_create(self: Any, data: Any)

def login(self: Any)

def message_command(self: Any, name: typing.Optional[str])

def message_create(self: Any, data: <class 'dict'>)Event fired when messages are created


def ready(self: Any, data: <class 'dict'>)

def reconnect(self: Any)

def request_guild_members(self: Any, guild_id: <class 'int'>, query: typing.Optional[str], limit: typing.Optional[int], presences: typing.Optional[bool], user_ids: typing.Optional[typing.List[str]], nonce: typing.Optional[str])

def resume(self: Any)

def send_json(self: Any, json: <class 'dict'>)

def unload_section(self: Any, section: typing.Union[EpikCord.CommandsSection, EpikCord.EventsSection])

def user_command(self: Any, name: typing.Optional[str])

def voice_server_update(self: Any, data: <class 'dict'>)

def wait_for(self: Any, event_name: <class 'str'>, check: typing.Optional[<built-in function callable>], timeout: typing.Union[float, int, NoneType])


ClientApplication
-----------------

def bulk_overwrite_global_application_commands(self: Any, commands: typing.List[EpikCord.ApplicationCommand])

def bulk_overwrite_guild_application_commands(self: Any, guild_id: <class 'str'>, commands: typing.List[EpikCord.ApplicationCommand])

def create_global_application_command(self: Any, name: <class 'str'>, description: <class 'str'>, options: typing.Optional[typing.List[typing.Union[EpikCord.options.Subcommand, EpikCord.options.SubCommandGroup, EpikCord.options.StringOption, EpikCord.options.IntegerOption, EpikCord.options.BooleanOption, EpikCord.options.UserOption, EpikCord.options.ChannelOption, EpikCord.options.RoleOption, EpikCord.options.MentionableOption, EpikCord.options.NumberOption]]], default_permission: typing.Optional[bool], command_type: typing.Optional[int])

def create_guild_application_command(self: Any, guild_id: <class 'str'>, name: <class 'str'>, description: <class 'str'>, options: typing.Optional[typing.List[typing.Union[EpikCord.options.Subcommand, EpikCord.options.SubCommandGroup, EpikCord.options.StringOption, EpikCord.options.IntegerOption, EpikCord.options.BooleanOption, EpikCord.options.UserOption, EpikCord.options.ChannelOption, EpikCord.options.RoleOption, EpikCord.options.MentionableOption, EpikCord.options.NumberOption]]], default_permission: typing.Optional[bool], command_type: typing.Optional[int])

def delete_global_application_command(self: Any, command_id: <class 'str'>)

def delete_guild_application_command(self: Any, guild_id: <class 'str'>, command_id: <class 'str'>)

def edit_application_command_permissions(self: Any, guild_id: <class 'str'>, command_id: Any, permissions: typing.List[EpikCord.ApplicationCommandPermission])

def edit_global_application_command(self: Any, guild_id: <class 'str'>, command_id: <class 'str'>, name: typing.Optional[str], description: typing.Optional[str], options: typing.Optional[typing.List[typing.Union[EpikCord.options.Subcommand, EpikCord.options.SubCommandGroup, EpikCord.options.StringOption, EpikCord.options.IntegerOption, EpikCord.options.BooleanOption, EpikCord.options.UserOption, EpikCord.options.ChannelOption, EpikCord.options.RoleOption, EpikCord.options.MentionableOption, EpikCord.options.NumberOption]]], default_permissions: typing.Optional[bool])

def fetch_application(self: Any)

def fetch_application_command(self: Any, command_id: <class 'str'>)

def fetch_global_application_commands(self: Any)

def fetch_guild_application_command(self: Any, guild_id: <class 'str'>, command_id: <class 'str'>)

def fetch_guild_application_command_permissions(self: Any, guild_id: <class 'str'>, command_id: <class 'str'>)

def fetch_guild_application_commands(self: Any, guild_id: <class 'str'>)


ClientMessageCommand
--------------------


ClientResponse
--------------

def close(self: Any)

def get_encoding(self: Any)

def json(self: Any, encoding: typing.Optional[str], loads: typing.Callable[[str], typing.Any], content_type: typing.Optional[str])Read and decodes JSON response.


def raise_for_status(self: Any)

def read(self: Any)Read response payload.


def release(self: Any)

def start(self: Any, connection: Connection)Start response processing.


def text(self: Any, encoding: typing.Optional[str], errors: <class 'str'>)Read response payload and decode.


def wait_for_close(self: Any)


ClientSession
-------------

def close(self: Any)Close underlying connector.

        Release all acquired resources.
        


def delete(self: Any, url: typing.Union[str, yarl.URL], kwargs: typing.Any)Perform HTTP DELETE request.


def detach(self: Any)Detach connector from session without closing the former.

        Session is switched to closed state anyway.
        


def get(self: Any, url: typing.Union[str, yarl.URL], allow_redirects: <class 'bool'>, kwargs: typing.Any)Perform HTTP GET request.


def head(self: Any, url: typing.Union[str, yarl.URL], allow_redirects: <class 'bool'>, kwargs: typing.Any)Perform HTTP HEAD request.


def options(self: Any, url: typing.Union[str, yarl.URL], allow_redirects: <class 'bool'>, kwargs: typing.Any)Perform HTTP OPTIONS request.


def patch(self: Any, url: typing.Union[str, yarl.URL], data: typing.Any, kwargs: typing.Any)Perform HTTP PATCH request.


def post(self: Any, url: typing.Union[str, yarl.URL], data: typing.Any, kwargs: typing.Any)Perform HTTP POST request.


def put(self: Any, url: typing.Union[str, yarl.URL], data: typing.Any, kwargs: typing.Any)Perform HTTP PUT request.


def request(self: Any, method: <class 'str'>, url: typing.Union[str, yarl.URL], kwargs: typing.Any)Perform HTTP request.


def ws_connect(self: Any, url: typing.Union[str, yarl.URL], method: <class 'str'>, protocols: typing.Iterable[str], timeout: <class 'float'>, receive_timeout: typing.Optional[float], autoclose: <class 'bool'>, autoping: <class 'bool'>, heartbeat: typing.Optional[float], auth: typing.Optional[aiohttp.helpers.BasicAuth], origin: typing.Optional[str], params: typing.Optional[typing.Mapping[str, str]], headers: typing.Union[typing.Mapping[typing.Union[str, multidict._multidict.istr], str], multidict._multidict.CIMultiDict, multidict._multidict.CIMultiDictProxy, NoneType], proxy: typing.Union[str, yarl.URL, NoneType], proxy_auth: typing.Optional[aiohttp.helpers.BasicAuth], ssl: typing.Union[ssl.SSLContext, bool, NoneType, aiohttp.client_reqrep.Fingerprint], verify_ssl: typing.Optional[bool], fingerprint: typing.Optional[bytes], ssl_context: typing.Optional[ssl.SSLContext], proxy_headers: typing.Union[typing.Mapping[typing.Union[str, multidict._multidict.istr], str], multidict._multidict.CIMultiDict, multidict._multidict.CIMultiDictProxy, NoneType], compress: <class 'int'>, max_msg_size: <class 'int'>)Initiate websocket connection.



ClientSlashCommand
------------------

def option_autocomplete(self: Any, option_name: <class 'str'>)


ClientUser
----------

def edit(self: Any, username: typing.Optional[str], avatar: typing.Optional[bytes])

def fetch(self: Any)


ClientUserCommand
-----------------


ClosedWebSocketConnection
-------------------------


Colour
------

def to_rgb(self: Any)Returns an rgb color as a tuple



Colour
------

def to_rgb(self: Any)Returns an rgb color as a tuple



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

def add_field(self: Any, name: <class 'str'>, value: <class 'str'>, inline: <class 'bool'>)

def set_author(self: Any, name: typing.Optional[str], url: typing.Optional[str], icon_url: typing.Optional[str], proxy_icon_url: typing.Optional[str])

def set_color(self: Any, colour: <class 'EpikCord.Colour'>)

def set_description(self: Any, description: typing.Optional[str])

def set_fields(self: Any, fields: typing.List[dict])

def set_footer(self: Any, text: typing.Optional[str], icon_url: typing.Optional[str], proxy_icon_url: typing.Optional[str])

def set_image(self: Any, url: typing.Optional[str], proxy_url: typing.Optional[str], height: typing.Optional[int], width: typing.Optional[int])

def set_provider(self: Any, name: typing.Optional[str], url: typing.Optional[str])

def set_thumbnail(self: Any, url: typing.Optional[str], proxy_url: typing.Optional[str], height: typing.Optional[int], width: typing.Optional[int])

def set_timestamp(self: Any, timestamp: <class 'datetime.datetime'>)

def set_title(self: Any, title: typing.Optional[str])

def set_url(self: Any, url: typing.Optional[str])

def set_video(self: Any, url: typing.Optional[str], proxy_url: typing.Optional[str], height: typing.Optional[int], width: typing.Optional[int])

def to_dict(self: Any)


Emoji
-----

def delete(self: Any, reason: typing.Optional[str])

def edit(self: Any, name: typing.Optional[str], roles: typing.Optional[typing.List[EpikCord.Role]], reason: typing.Optional[str])


EpikCordException
-----------------


EventHandler
------------

def channel_create(self: Any, data: <class 'dict'>)

def component(self: Any, custom_id: <class 'str'>)
        Execute this function when a component with the `custom_id` is interacted with.
        


def event(self: Any, func: Any)

def get_event_callback(self: Any, event_name: <class 'str'>, internal: Any)

def guild_create(self: Any, data: Any)

def guild_delete(self: Any, data: <class 'dict'>)

def guild_member_update(self: Any, data: Any)

def guild_members_chunk(self: Any, data: <class 'dict'>)

def handle_event(self: Any, event_name: typing.Optional[str], data: <class 'dict'>)

def handle_events(self: Any)

def interaction_create(self: Any, data: Any)

def message_create(self: Any, data: <class 'dict'>)Event fired when messages are created


def ready(self: Any, data: <class 'dict'>)

def voice_server_update(self: Any, data: <class 'dict'>)

def wait_for(self: Any, event_name: <class 'str'>, check: typing.Optional[<built-in function callable>], timeout: typing.Union[float, int, NoneType])


EventsSection
-------------


FailedToConnectToVoice
----------------------


File
----


Flag
----

def calculate_from_turned(self: Any)


Forbidden403
------------


GateawayUnavailable502
----------------------


Guild
-----

def create_channel(self: Any, name: <class 'str'>, reason: typing.Optional[str], type: typing.Optional[int], topic: typing.Optional[str], bitrate: typing.Optional[int], user_limit: typing.Optional[int], rate_limit_per_user: typing.Optional[int], position: typing.Optional[int], permission_overwrites: typing.List[typing.Optional[EpikCord.Overwrite]], parent_id: typing.Optional[str], nsfw: typing.Optional[bool])Creates a channel.

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
        


def delete(self: Any)

def edit(self: Any, name: typing.Optional[str], verification_level: typing.Optional[int], default_message_notifications: typing.Optional[int], explicit_content_filter: typing.Optional[int], afk_channel_id: typing.Optional[str], afk_timeout: typing.Optional[int], owner_id: typing.Optional[str], system_channel_id: typing.Optional[str], system_channel_flags: typing.Optional[EpikCord.SystemChannelFlags], rules_channel_id: typing.Optional[str], preferred_locale: typing.Optional[str], features: typing.Optional[typing.List[str]], description: typing.Optional[str], premium_progress_bar_enabled: typing.Optional[bool], reason: typing.Optional[str])Edits the guild.

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
        


def fetch_channels(self: Any)Fetches the guild channels.

        Returns
        -------
        List[GuildChannel]
            The guild channels.
        


def fetch_guild_preview(self: Any)Fetches the guild preview.

        Returns
        -------
        GuildPreview
            The guild preview.
        



GuildApplicationCommandPermission
---------------------------------

def to_dict(self: Any)


GuildBan
--------


GuildChannel
------------

def create_invite(self: Any, max_age: typing.Optional[int], max_uses: typing.Optional[int], temporary: typing.Optional[bool], unique: typing.Optional[bool], target_type: typing.Optional[int], target_user_id: typing.Optional[str], target_application_id: typing.Optional[str])

def delete(self: Any, reason: typing.Optional[str])

def delete_overwrite(self: Any, overwrites: <class 'EpikCord.Overwrite'>)

def fetch_invites(self: Any)

def fetch_pinned_messages(self: Any)


GuildManager
------------

def add_to_cache(self: Any, key: Any, value: Any)

def clear_cache(self: Any)

def fetch(self: Any, guild_id: <class 'str'>, skip_cache: typing.Optional[bool], with_counts: typing.Optional[bool])

def format_cache(self: Any)

def get_from_cache(self: Any, key: Any)

def is_in_cache(self: Any, key: Any)

def remove_from_cache(self: Any, key: Any)


GuildMember
-----------

def fetch_message(self: Any, message_id: <class 'str'>)

def fetch_messages(self: Any, around: typing.Optional[str], before: typing.Optional[str], after: typing.Optional[str], limit: typing.Optional[int])

def send(self: Any, content: typing.Optional[str], embeds: typing.Optional[typing.List[dict]], components: Any, tts: typing.Optional[bool], allowed_mentions: Any, sticker_ids: typing.Optional[typing.List[str]], attachments: typing.List[EpikCord.File], suppress_embeds: <class 'bool'>)


GuildNewsChannel
----------------

def bulk_delete(self: Any, message_ids: typing.List[str], reason: typing.Optional[str])

def create_invite(self: Any, max_age: typing.Optional[int], max_uses: typing.Optional[int], temporary: typing.Optional[bool], unique: typing.Optional[bool], target_type: typing.Optional[int], target_user_id: typing.Optional[str], target_application_id: typing.Optional[str])

def create_webhook(self: Any, name: <class 'str'>, avatar: typing.Optional[str], reason: typing.Optional[str])

def delete(self: Any, reason: typing.Optional[str])

def delete_overwrite(self: Any, overwrites: <class 'EpikCord.Overwrite'>)

def fetch_invites(self: Any)

def fetch_message(self: Any, message_id: <class 'str'>)

def fetch_messages(self: Any, around: typing.Optional[str], before: typing.Optional[str], after: typing.Optional[str], limit: typing.Optional[int])

def fetch_pinned_messages(self: Any)

def follow(self: Any, webhook_channel_id: <class 'str'>)

def list_joined_private_archived_threads(self: Any, before: typing.Optional[str], limit: typing.Optional[int])

def list_private_archived_threads(self: Any, before: typing.Optional[str], limit: typing.Optional[int])

def list_public_archived_threads(self: Any, before: typing.Optional[str], limit: typing.Optional[int])

def send(self: Any, content: typing.Optional[str], embeds: typing.Optional[typing.List[dict]], components: Any, tts: typing.Optional[bool], allowed_mentions: Any, sticker_ids: typing.Optional[typing.List[str]], attachments: typing.List[EpikCord.File], suppress_embeds: <class 'bool'>)

def start_thread(self: Any, name: <class 'str'>, auto_archive_duration: typing.Optional[int], type: typing.Optional[int], invitable: typing.Optional[bool], rate_limit_per_user: typing.Optional[int], reason: typing.Optional[str])


GuildNewsThread
---------------

def add_member(self: Any, member_id: <class 'str'>)

def bulk_delete(self: Any, message_ids: typing.List[str], reason: typing.Optional[str])

def create_invite(self: Any, max_age: typing.Optional[int], max_uses: typing.Optional[int], temporary: typing.Optional[bool], unique: typing.Optional[bool], target_type: typing.Optional[int], target_user_id: typing.Optional[str], target_application_id: typing.Optional[str])

def create_webhook(self: Any, name: <class 'str'>, avatar: typing.Optional[str], reason: typing.Optional[str])

def delete(self: Any, reason: typing.Optional[str])

def delete_overwrite(self: Any, overwrites: <class 'EpikCord.Overwrite'>)

def fetch_invites(self: Any)

def fetch_member(self: Any, member_id: <class 'str'>)

def fetch_message(self: Any, message_id: <class 'str'>)

def fetch_messages(self: Any, around: typing.Optional[str], before: typing.Optional[str], after: typing.Optional[str], limit: typing.Optional[int])

def fetch_pinned_messages(self: Any)

def follow(self: Any, webhook_channel_id: <class 'str'>)

def join(self: Any)

def leave(self: Any)

def list_joined_private_archived_threads(self: Any, before: typing.Optional[str], limit: typing.Optional[int])

def list_members(self: Any)

def list_private_archived_threads(self: Any, before: typing.Optional[str], limit: typing.Optional[int])

def list_public_archived_threads(self: Any, before: typing.Optional[str], limit: typing.Optional[int])

def remove_member(self: Any, member_id: <class 'str'>)

def send(self: Any, content: typing.Optional[str], embeds: typing.Optional[typing.List[dict]], components: Any, tts: typing.Optional[bool], allowed_mentions: Any, sticker_ids: typing.Optional[typing.List[str]], attachments: typing.List[EpikCord.File], suppress_embeds: <class 'bool'>)

def start_thread(self: Any, name: <class 'str'>, auto_archive_duration: typing.Optional[int], type: typing.Optional[int], invitable: typing.Optional[bool], rate_limit_per_user: typing.Optional[int], reason: typing.Optional[str])


GuildPreview
------------


GuildScheduledEvent
-------------------


GuildStageChannel
-----------------


GuildTextChannel
----------------

def bulk_delete(self: Any, message_ids: typing.List[str], reason: typing.Optional[str])

def create_invite(self: Any, max_age: typing.Optional[int], max_uses: typing.Optional[int], temporary: typing.Optional[bool], unique: typing.Optional[bool], target_type: typing.Optional[int], target_user_id: typing.Optional[str], target_application_id: typing.Optional[str])

def create_webhook(self: Any, name: <class 'str'>, avatar: typing.Optional[str], reason: typing.Optional[str])

def delete(self: Any, reason: typing.Optional[str])

def delete_overwrite(self: Any, overwrites: <class 'EpikCord.Overwrite'>)

def fetch_invites(self: Any)

def fetch_message(self: Any, message_id: <class 'str'>)

def fetch_messages(self: Any, around: typing.Optional[str], before: typing.Optional[str], after: typing.Optional[str], limit: typing.Optional[int])

def fetch_pinned_messages(self: Any)

def list_joined_private_archived_threads(self: Any, before: typing.Optional[str], limit: typing.Optional[int])

def list_private_archived_threads(self: Any, before: typing.Optional[str], limit: typing.Optional[int])

def list_public_archived_threads(self: Any, before: typing.Optional[str], limit: typing.Optional[int])

def send(self: Any, content: typing.Optional[str], embeds: typing.Optional[typing.List[dict]], components: Any, tts: typing.Optional[bool], allowed_mentions: Any, sticker_ids: typing.Optional[typing.List[str]], attachments: typing.List[EpikCord.File], suppress_embeds: <class 'bool'>)

def start_thread(self: Any, name: <class 'str'>, auto_archive_duration: typing.Optional[int], type: typing.Optional[int], invitable: typing.Optional[bool], rate_limit_per_user: typing.Optional[int], reason: typing.Optional[str])


GuildWidget
-----------


GuildWidgetSettings
-------------------


HTTPClient
----------

def close(self: Any)Close underlying connector.

        Release all acquired resources.
        


def delete(self: Any, url: Any, args: Any, to_discord: <class 'bool'>, kwargs: Any)

def detach(self: Any)Detach connector from session without closing the former.

        Session is switched to closed state anyway.
        


def get(self: Any, url: Any, args: Any, to_discord: <class 'bool'>, kwargs: Any)

def head(self: Any, url: Any, args: Any, to_discord: <class 'bool'>, kwargs: Any)

def log_request(self: Any, res: Any)

def options(self: Any, url: typing.Union[str, yarl.URL], allow_redirects: <class 'bool'>, kwargs: typing.Any)Perform HTTP OPTIONS request.


def patch(self: Any, url: Any, args: Any, to_discord: <class 'bool'>, kwargs: Any)

def post(self: Any, url: Any, args: Any, to_discord: <class 'bool'>, kwargs: Any)

def put(self: Any, url: Any, args: Any, to_discord: <class 'bool'>, kwargs: Any)

def request(self: Any, method: <class 'str'>, url: typing.Union[str, yarl.URL], kwargs: typing.Any)Perform HTTP request.


def ws_connect(self: Any, url: typing.Union[str, yarl.URL], method: <class 'str'>, protocols: typing.Iterable[str], timeout: <class 'float'>, receive_timeout: typing.Optional[float], autoclose: <class 'bool'>, autoping: <class 'bool'>, heartbeat: typing.Optional[float], auth: typing.Optional[aiohttp.helpers.BasicAuth], origin: typing.Optional[str], params: typing.Optional[typing.Mapping[str, str]], headers: typing.Union[typing.Mapping[typing.Union[str, multidict._multidict.istr], str], multidict._multidict.CIMultiDict, multidict._multidict.CIMultiDictProxy, NoneType], proxy: typing.Union[str, yarl.URL, NoneType], proxy_auth: typing.Optional[aiohttp.helpers.BasicAuth], ssl: typing.Union[ssl.SSLContext, bool, NoneType, aiohttp.client_reqrep.Fingerprint], verify_ssl: typing.Optional[bool], fingerprint: typing.Optional[bytes], ssl_context: typing.Optional[ssl.SSLContext], proxy_headers: typing.Union[typing.Mapping[typing.Union[str, multidict._multidict.istr], str], multidict._multidict.CIMultiDict, multidict._multidict.CIMultiDictProxy, NoneType], compress: <class 'int'>, max_msg_size: <class 'int'>)Initiate websocket connection.



IntegerOption
-------------

def to_dict(self: Any)


Integration
-----------


IntegrationAccount
------------------


Intents
-------

def calculate_from_turned(self: Any)


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

def to_dict(self: Any)


MentionedChannel
----------------


MentionedUser
-------------

def fetch_message(self: Any, message_id: <class 'str'>)

def fetch_messages(self: Any, around: typing.Optional[str], before: typing.Optional[str], after: typing.Optional[str], limit: typing.Optional[int])

def send(self: Any, content: typing.Optional[str], embeds: typing.Optional[typing.List[dict]], components: Any, tts: typing.Optional[bool], allowed_mentions: Any, sticker_ids: typing.Optional[typing.List[str]], attachments: typing.List[EpikCord.File], suppress_embeds: <class 'bool'>)


Message
-------

def add_reaction(self: Any, emoji: <class 'str'>)

def crosspost(self: Any)

def delete(self: Any)

def delete_all_reactions(self: Any)

def delete_reaction_for_emoji(self: Any, emoji: <class 'str'>)

def edit(self: Any, message_data: <class 'dict'>)

def fetch_reactions(self: Any, after: Any, limit: Any)

def pin(self: Any, reason: typing.Optional[str])

def remove_reaction(self: Any, emoji: <class 'str'>, user: Any)

def start_thread(self: Any, name: <class 'str'>, auto_archive_duration: typing.Optional[int], rate_limit_per_user: typing.Optional[int])

def unpin(self: Any, reason: typing.Optional[str])


MessageActivity
---------------


MessageCommandInteraction
-------------------------

def create_followup(self: Any, tts: <class 'bool'>, content: typing.Optional[str], embeds: typing.Optional[typing.List[EpikCord.Embed]], allowed_mentions: Any, components: typing.Optional[typing.List[typing.Union[EpikCord.components.Button, EpikCord.components.SelectMenu, EpikCord.components.TextInput]]], attachments: typing.Optional[typing.List[EpikCord.Attachment]], suppress_embeds: typing.Optional[bool], ephemeral: typing.Optional[bool])

def defer(self: Any, show_loading_state: typing.Optional[bool])

def delete_followup(self: Any)

def delete_original_response(self: Any)

def edit_followup(self: Any, tts: <class 'bool'>, content: typing.Optional[str], embeds: typing.Optional[typing.List[EpikCord.Embed]], allowed_mentions: Any, components: typing.Optional[typing.List[typing.Union[EpikCord.components.Button, EpikCord.components.SelectMenu, EpikCord.components.TextInput]]], attachments: typing.Optional[typing.List[EpikCord.Attachment]], suppress_embeds: typing.Optional[bool], ephemeral: typing.Optional[bool])

def edit_original_response(self: Any, tts: <class 'bool'>, content: typing.Optional[str], embeds: typing.Optional[typing.List[EpikCord.Embed]], allowed_mentions: Any, components: typing.Optional[typing.List[typing.Union[EpikCord.components.Button, EpikCord.components.SelectMenu, EpikCord.components.TextInput]]], attachments: typing.Optional[typing.List[EpikCord.Attachment]], suppress_embeds: typing.Optional[bool], ephemeral: typing.Optional[bool])

def fetch_original_response(self: Any, skip_cache: typing.Optional[bool])

def is_application_command(self: Any)

def is_autocomplete(self: Any)

def is_message_component(self: Any)

def is_modal_submit(self: Any)

def is_ping(self: Any)

def reply(self: Any, tts: <class 'bool'>, content: typing.Optional[str], embeds: typing.Optional[typing.List[EpikCord.Embed]], allowed_mentions: Any, components: typing.Optional[typing.List[typing.Union[EpikCord.components.Button, EpikCord.components.SelectMenu, EpikCord.components.TextInput]]], attachments: typing.Optional[typing.List[EpikCord.Attachment]], suppress_embeds: typing.Optional[bool], ephemeral: typing.Optional[bool])

def send_modal(self: Any, modal: <class 'EpikCord.Modal'>)


MessageComponentInteraction
---------------------------

def create_followup(self: Any, tts: <class 'bool'>, content: typing.Optional[str], embeds: typing.Optional[typing.List[EpikCord.Embed]], allowed_mentions: Any, components: typing.Optional[typing.List[typing.Union[EpikCord.components.Button, EpikCord.components.SelectMenu, EpikCord.components.TextInput]]], attachments: typing.Optional[typing.List[EpikCord.Attachment]], suppress_embeds: typing.Optional[bool], ephemeral: typing.Optional[bool])

def defer(self: Any, show_loading_state: typing.Optional[bool])

def defer_update(self: Any)

def delete_followup(self: Any)

def delete_original_response(self: Any)

def edit_followup(self: Any, tts: <class 'bool'>, content: typing.Optional[str], embeds: typing.Optional[typing.List[EpikCord.Embed]], allowed_mentions: Any, components: typing.Optional[typing.List[typing.Union[EpikCord.components.Button, EpikCord.components.SelectMenu, EpikCord.components.TextInput]]], attachments: typing.Optional[typing.List[EpikCord.Attachment]], suppress_embeds: typing.Optional[bool], ephemeral: typing.Optional[bool])

def edit_original_response(self: Any, tts: <class 'bool'>, content: typing.Optional[str], embeds: typing.Optional[typing.List[EpikCord.Embed]], allowed_mentions: Any, components: typing.Optional[typing.List[typing.Union[EpikCord.components.Button, EpikCord.components.SelectMenu, EpikCord.components.TextInput]]], attachments: typing.Optional[typing.List[EpikCord.Attachment]], suppress_embeds: typing.Optional[bool], ephemeral: typing.Optional[bool])

def fetch_original_response(self: Any, skip_cache: typing.Optional[bool])

def is_action_row(self: Any)

def is_application_command(self: Any)

def is_autocomplete(self: Any)

def is_button(self: Any)

def is_message_component(self: Any)

def is_modal_submit(self: Any)

def is_ping(self: Any)

def is_select_menu(self: Any)

def is_text_input(self: Any)

def reply(self: Any, tts: <class 'bool'>, content: typing.Optional[str], embeds: typing.Optional[typing.List[EpikCord.Embed]], allowed_mentions: Any, components: typing.Optional[typing.List[typing.Union[EpikCord.components.Button, EpikCord.components.SelectMenu, EpikCord.components.TextInput]]], attachments: typing.Optional[typing.List[EpikCord.Attachment]], suppress_embeds: typing.Optional[bool], ephemeral: typing.Optional[bool])

def send_modal(self: Any, modal: <class 'EpikCord.Modal'>)

def update(self: Any, tts: <class 'bool'>, content: typing.Optional[str], embeds: typing.Optional[typing.List[EpikCord.Embed]], allowed_mentions: Any, components: typing.Optional[typing.List[typing.Union[EpikCord.components.Button, EpikCord.components.SelectMenu, EpikCord.components.TextInput]]], attachments: typing.Optional[typing.List[EpikCord.Attachment]], suppress_embeds: typing.Optional[bool])


MessageInteraction
------------------


Messageable
-----------

def fetch_message(self: Any, message_id: <class 'str'>)

def fetch_messages(self: Any, around: typing.Optional[str], before: typing.Optional[str], after: typing.Optional[str], limit: typing.Optional[int])

def send(self: Any, content: typing.Optional[str], embeds: typing.Optional[typing.List[dict]], components: Any, tts: typing.Optional[bool], allowed_mentions: Any, sticker_ids: typing.Optional[typing.List[str]], attachments: typing.List[EpikCord.File], suppress_embeds: <class 'bool'>)


MethodNotAllowed405
-------------------


MissingClientSetting
--------------------


MissingCustomId
---------------


Modal
-----

def to_dict(self: Any)


ModalSubmitInteraction
----------------------

def create_followup(self: Any, tts: <class 'bool'>, content: typing.Optional[str], embeds: typing.Optional[typing.List[EpikCord.Embed]], allowed_mentions: Any, components: typing.Optional[typing.List[typing.Union[EpikCord.components.Button, EpikCord.components.SelectMenu, EpikCord.components.TextInput]]], attachments: typing.Optional[typing.List[EpikCord.Attachment]], suppress_embeds: typing.Optional[bool], ephemeral: typing.Optional[bool])

def defer(self: Any, show_loading_state: typing.Optional[bool])

def delete_followup(self: Any)

def delete_original_response(self: Any)

def edit_followup(self: Any, tts: <class 'bool'>, content: typing.Optional[str], embeds: typing.Optional[typing.List[EpikCord.Embed]], allowed_mentions: Any, components: typing.Optional[typing.List[typing.Union[EpikCord.components.Button, EpikCord.components.SelectMenu, EpikCord.components.TextInput]]], attachments: typing.Optional[typing.List[EpikCord.Attachment]], suppress_embeds: typing.Optional[bool], ephemeral: typing.Optional[bool])

def edit_original_response(self: Any, tts: <class 'bool'>, content: typing.Optional[str], embeds: typing.Optional[typing.List[EpikCord.Embed]], allowed_mentions: Any, components: typing.Optional[typing.List[typing.Union[EpikCord.components.Button, EpikCord.components.SelectMenu, EpikCord.components.TextInput]]], attachments: typing.Optional[typing.List[EpikCord.Attachment]], suppress_embeds: typing.Optional[bool], ephemeral: typing.Optional[bool])

def fetch_original_response(self: Any, skip_cache: typing.Optional[bool])

def is_application_command(self: Any)

def is_autocomplete(self: Any)

def is_message_component(self: Any)

def is_modal_submit(self: Any)

def is_ping(self: Any)

def reply(self: Any, tts: <class 'bool'>, content: typing.Optional[str], embeds: typing.Optional[typing.List[EpikCord.Embed]], allowed_mentions: Any, components: typing.Optional[typing.List[typing.Union[EpikCord.components.Button, EpikCord.components.SelectMenu, EpikCord.components.TextInput]]], attachments: typing.Optional[typing.List[EpikCord.Attachment]], suppress_embeds: typing.Optional[bool], ephemeral: typing.Optional[bool])

def send_modal(self: Any, args: Any, kwargs: Any)


NotFound404
-----------


NumberOption
------------

def to_dict(self: Any)


Overwrite
---------


Paginator
---------

def add_page(self: Any, page: <class 'EpikCord.Embed'>)

def back(self: Any)

def current(self: Any)

def forward(self: Any)

def remove_page(self: Any, page: <class 'EpikCord.Embed'>)


PartialEmoji
------------

def to_dict(self: Any)


PartialGuild
------------


PartialUser
-----------


Permissions
-----------

def calculate_from_turned(self: Any)


Presence
--------

def to_dict(self: Any)


PrivateThread
-------------

def add_member(self: Any, member_id: <class 'str'>)

def bulk_delete(self: Any, message_ids: typing.List[str], reason: typing.Optional[str])

def fetch_member(self: Any, member_id: <class 'str'>)

def join(self: Any)

def leave(self: Any)

def list_members(self: Any)

def remove_member(self: Any, member_id: <class 'str'>)


RatelimitHandler
----------------

def is_ratelimited(self: Any)
        Checks if the client is ratelimited.
        


def process_headers(self: Any, headers: <class 'dict'>)
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

def to_dict(self: Any)


RoleTag
-------


SelectMenu
----------

def add_options(self: Any, options: typing.List[EpikCord.components.SelectMenuOption])

def set_custom_id(self: Any, custom_id: <class 'str'>)

def set_disabled(self: Any, disabled: <class 'bool'>)

def set_max_values(self: Any, max: <class 'int'>)

def set_min_values(self: Any, min: <class 'int'>)

def set_placeholder(self: Any, placeholder: <class 'str'>)

def to_dict(self: Any)


SelectMenuOption
----------------

def to_dict(self: Any)


Shard
-----

def change_presence(self: Any, presence: typing.Optional[EpikCord.Presence])

def channel_create(self: Any, data: <class 'dict'>)

def close(self: Any)

def component(self: Any, custom_id: <class 'str'>)
        Execute this function when a component with the `custom_id` is interacted with.
        


def connect(self: Any)

def event(self: Any, func: Any)

def get_event_callback(self: Any, event_name: <class 'str'>, internal: Any)

def guild_create(self: Any, data: Any)

def guild_delete(self: Any, data: <class 'dict'>)

def guild_member_update(self: Any, data: Any)

def guild_members_chunk(self: Any, data: <class 'dict'>)

def handle_close(self: Any)

def handle_event(self: Any, event_name: typing.Optional[str], data: <class 'dict'>)

def handle_events(self: Any)

def heartbeat(self: Any, forced: typing.Optional[bool])

def identify(self: Any)

def interaction_create(self: Any, data: Any)

def login(self: Any)

def message_create(self: Any, data: <class 'dict'>)Event fired when messages are created


def ready(self: Any, data: <class 'dict'>)

def reconnect(self: Any)

def request_guild_members(self: Any, guild_id: <class 'int'>, query: typing.Optional[str], limit: typing.Optional[int], presences: typing.Optional[bool], user_ids: typing.Optional[typing.List[str]], nonce: typing.Optional[str])

def resume(self: Any)

def send_json(self: Any, json: <class 'dict'>)

def voice_server_update(self: Any, data: <class 'dict'>)

def wait_for(self: Any, event_name: <class 'str'>, check: typing.Optional[<built-in function callable>], timeout: typing.Union[float, int, NoneType])


ShardingRequired
----------------


SlashCommand
------------

def to_dict(self: Any)


SlashCommandOptionChoice
------------------------

def to_dict(self: Any)


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

def to_dict(self: Any)


SubCommandGroup
---------------

def to_dict(self: Any)


Subcommand
----------

def to_dict(self: Any)


SystemChannelFlags
------------------


Team
----


TeamMember
----------


TextInput
---------

def set_custom_id(self: Any, custom_id: <class 'str'>)

def to_dict(self: Any)


Thread
------

def add_member(self: Any, member_id: <class 'str'>)

def bulk_delete(self: Any, message_ids: typing.List[str], reason: typing.Optional[str])

def fetch_member(self: Any, member_id: <class 'str'>)

def join(self: Any)

def leave(self: Any)

def list_members(self: Any)

def remove_member(self: Any, member_id: <class 'str'>)


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

def fetch_message(self: Any, message_id: <class 'str'>)

def fetch_messages(self: Any, around: typing.Optional[str], before: typing.Optional[str], after: typing.Optional[str], limit: typing.Optional[int])

def send(self: Any, content: typing.Optional[str], embeds: typing.Optional[typing.List[dict]], components: Any, tts: typing.Optional[bool], allowed_mentions: Any, sticker_ids: typing.Optional[typing.List[str]], attachments: typing.List[EpikCord.File], suppress_embeds: <class 'bool'>)


UserCommandInteraction
----------------------

def create_followup(self: Any, tts: <class 'bool'>, content: typing.Optional[str], embeds: typing.Optional[typing.List[EpikCord.Embed]], allowed_mentions: Any, components: typing.Optional[typing.List[typing.Union[EpikCord.components.Button, EpikCord.components.SelectMenu, EpikCord.components.TextInput]]], attachments: typing.Optional[typing.List[EpikCord.Attachment]], suppress_embeds: typing.Optional[bool], ephemeral: typing.Optional[bool])

def defer(self: Any, show_loading_state: typing.Optional[bool])

def delete_followup(self: Any)

def delete_original_response(self: Any)

def edit_followup(self: Any, tts: <class 'bool'>, content: typing.Optional[str], embeds: typing.Optional[typing.List[EpikCord.Embed]], allowed_mentions: Any, components: typing.Optional[typing.List[typing.Union[EpikCord.components.Button, EpikCord.components.SelectMenu, EpikCord.components.TextInput]]], attachments: typing.Optional[typing.List[EpikCord.Attachment]], suppress_embeds: typing.Optional[bool], ephemeral: typing.Optional[bool])

def edit_original_response(self: Any, tts: <class 'bool'>, content: typing.Optional[str], embeds: typing.Optional[typing.List[EpikCord.Embed]], allowed_mentions: Any, components: typing.Optional[typing.List[typing.Union[EpikCord.components.Button, EpikCord.components.SelectMenu, EpikCord.components.TextInput]]], attachments: typing.Optional[typing.List[EpikCord.Attachment]], suppress_embeds: typing.Optional[bool], ephemeral: typing.Optional[bool])

def fetch_original_response(self: Any, skip_cache: typing.Optional[bool])

def is_application_command(self: Any)

def is_autocomplete(self: Any)

def is_message_component(self: Any)

def is_modal_submit(self: Any)

def is_ping(self: Any)

def reply(self: Any, tts: <class 'bool'>, content: typing.Optional[str], embeds: typing.Optional[typing.List[EpikCord.Embed]], allowed_mentions: Any, components: typing.Optional[typing.List[typing.Union[EpikCord.components.Button, EpikCord.components.SelectMenu, EpikCord.components.TextInput]]], attachments: typing.Optional[typing.List[EpikCord.Attachment]], suppress_embeds: typing.Optional[bool], ephemeral: typing.Optional[bool])

def send_modal(self: Any, modal: <class 'EpikCord.Modal'>)


UserOption
----------

def to_dict(self: Any)


Utils
-----

def cancel_tasks(self: Any, loop: Any)

def channel_from_type(self: Any, channel_data: <class 'dict'>)

def cleanup_loop(self: Any, loop: Any)

def component_from_type(self: Any, component_data: <class 'dict'>)

def compute_timedelta(self: Any, dt: <class 'datetime.datetime'>)

def escape_markdown(self: Any, text: <class 'str'>, as_needed: <class 'bool'>, ignore_links: <class 'bool'>)

def escape_mentions(self: Any, text: <class 'str'>)

def get_mime_type_for_image(self: Any, data: <class 'bytes'>)

def interaction_from_type(self: Any, data: Any)

def remove_markdown(self: Any, text: <class 'str'>, ignore_links: <class 'bool'>)

def sleep_until(self: Any, when: typing.Union[datetime.datetime, int, float], result: typing.Optional[~T])

def utcnow(self: Any)


VoiceChannel
------------

def create_invite(self: Any, max_age: typing.Optional[int], max_uses: typing.Optional[int], temporary: typing.Optional[bool], unique: typing.Optional[bool], target_type: typing.Optional[int], target_user_id: typing.Optional[str], target_application_id: typing.Optional[str])

def delete(self: Any, reason: typing.Optional[str])

def delete_overwrite(self: Any, overwrites: <class 'EpikCord.Overwrite'>)

def fetch_invites(self: Any)

def fetch_pinned_messages(self: Any)


VoiceState
----------


VoiceWebsocketClient
--------------------

def connect(self: Any, muted: typing.Optional[bool], deafened: typing.Optional[bool])


Webhook
-------


WebhookUser
-----------


WebsocketClient
---------------

def change_presence(self: Any, presence: typing.Optional[EpikCord.Presence])

def channel_create(self: Any, data: <class 'dict'>)

def close(self: Any)

def component(self: Any, custom_id: <class 'str'>)
        Execute this function when a component with the `custom_id` is interacted with.
        


def connect(self: Any)

def event(self: Any, func: Any)

def get_event_callback(self: Any, event_name: <class 'str'>, internal: Any)

def guild_create(self: Any, data: Any)

def guild_delete(self: Any, data: <class 'dict'>)

def guild_member_update(self: Any, data: Any)

def guild_members_chunk(self: Any, data: <class 'dict'>)

def handle_close(self: Any)

def handle_event(self: Any, event_name: typing.Optional[str], data: <class 'dict'>)

def handle_events(self: Any)

def heartbeat(self: Any, forced: typing.Optional[bool])

def identify(self: Any)

def interaction_create(self: Any, data: Any)

def login(self: Any)

def message_create(self: Any, data: <class 'dict'>)Event fired when messages are created


def ready(self: Any, data: <class 'dict'>)

def reconnect(self: Any)

def request_guild_members(self: Any, guild_id: <class 'int'>, query: typing.Optional[str], limit: typing.Optional[int], presences: typing.Optional[bool], user_ids: typing.Optional[typing.List[str]], nonce: typing.Optional[str])

def resume(self: Any)

def send_json(self: Any, json: <class 'dict'>)

def voice_server_update(self: Any, data: <class 'dict'>)

def wait_for(self: Any, event_name: <class 'str'>, check: typing.Optional[<built-in function callable>], timeout: typing.Union[float, int, NoneType])


WelcomeScreen
-------------


WelcomeScreenChannel
--------------------
