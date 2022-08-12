from __future__ import annotations
from enum import IntFlag


class EpikCordFlag(IntFlag):
    @classmethod
    def all(cls) -> EpikCordFlag:
        value = 0

        for k in cls.__members__:
            value |= cls[k]

        return cls(value)


class Intents(EpikCordFlag):
    guilds = 1 << 0
    members = 1 << 1
    bans = 1 << 2
    emojis_and_stickers = 1 << 3
    integrations = 1 << 4
    webhooks = 1 << 5
    invites = 1 << 6
    voice_states = 1 << 7
    presences = 1 << 8

    guild_messages = 1 << 9
    guild_message_reactions = 1 << 10
    guild_message_typing = 1 << 11

    direct_messages = 1 << 12
    direct_message_reactions = 1 << 13
    direct_message_typing = 1 << 14

    message_content = 1 << 15
    scheduled_event = 1 << 16


class SystemChannelFlags(EpikCordFlag):

    suppress_join_notifications = 1 << 0
    suppress_premium_subscriptions = 1 << 1
    suppress_guild_reminder_notifications = 1 << 2
    suppress_join_notification_replies = 1 << 3


class Permissions(EpikCordFlag):
    create_instant_invite = 1 << 0
    kick_members = 1 << 1
    ban_members = 1 << 2
    administrator = 1 << 3
    manage_channels = 1 << 4
    manage_guild = 1 << 5
    add_reactions = 1 << 6
    view_audit_log = 1 << 7
    priority_speaker = 1 << 8
    stream = 1 << 9
    read_messages = 1 << 10
    send_messages = 1 << 11
    send_tts_messages = 1 << 12
    manage_messages = 1 << 13
    embed_links = 1 << 14
    attach_files = 1 << 15
    read_message_history = 1 << 16
    mention_everyone = 1 << 17
    use_external_emojis = 1 << 18
    connect = 1 << 20
    speak = 1 << 21
    mute_members = 1 << 22
    deafen_members = 1 << 23
    move_members = 1 << 24
    use_voice_activation = 1 << 25
    change_nickname = 1 << 26
    manage_nicknames = 1 << 27
    manage_roles = 1 << 28
    manage_webhooks = 1 << 29
    manage_emojis_and_stickers = 1 << 30
    use_application_commands = 1 << 31
    request_to_speak = 1 << 32
    manage_events = 1 << 33
    manage_threads = 1 << 34
    create_public_threads = 1 << 35
    create_private_threads = 1 << 36
    use_external_stickers = 1 << 37
    send_messages_in_threads = 1 << 38
    start_embedded_activities = 1 << 39
    moderator_members = 1 << 40


__all__ = ("Intents", "SystemChannelFlags", "Permissions", "EpikCordFlag")
