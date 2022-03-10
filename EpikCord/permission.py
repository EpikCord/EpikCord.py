class Permission:
    def __init__(self, *, bit: int = 0):
        self.value = bit

    @property
    def create_instant_invite(self):
        self.value += 1 << 0
        return self

    @property
    def kick_members(self):
        self.value += 1 << 1
        return self

    @property
    def ban_members(self):
        self.value += 1 << 2
        return self

    @property
    def administrator(self):
        self.value += 1 << 3
        return self

    @property
    def manage_channels(self):
        self.value += 1 << 4
        return self

    @property
    def manage_guild(self):
        self.value += 1 << 5
        return self

    @property
    def add_reactions(self):
        self.value += 1 << 6
        return self

    @property
    def view_audit_log(self):
        self.value += 1 << 7
        return self

    @property
    def priority_speaker(self):
        self.value += 1 << 8
        return self

    @property
    def stream(self):
        self.value += 1 << 9
        return self

    @property
    def read_messages(self):
        self.value += 1 << 10
        return self

    @property
    def send_messages(self):
        self.value += 1 << 11
        return self

    @property
    def send_tts_messages(self):
        self.value += 1 << 12
        return self

    @property
    def manage_messages(self):
        self.value += 1 << 13
        return self

    @property
    def embed_links(self):
        self.value += 1 << 14
        return self

    @property
    def attach_files(self):
        self.value += 1 << 15
        return self

    @property
    def read_message_history(self):
        self.value += 1 << 16
        return self

    @property
    def mention_everyone(self):
        self.value += 1 << 17
        return self

    @property
    def use_external_emojis(self):
        self.value += 1 << 18
        return self

    @property
    def connect(self):
        self.value += 1 << 20
        return self

    @property
    def speak(self):
        self.value += 1 << 21
        return self

    @property
    def mute_members(self):
        self.value += 1 << 22
        return self

    @property
    def deafen_members(self):
        self.value += 1 << 23
        return self

    @property
    def move_members(self):
        self.value += 1 << 24
        return self

    @property
    def use_voice_activation(self):
        self.value += 1 << 25
        return self

    @property
    def change_nickname(self):
        self.value += 1 << 26
        return self

    @property
    def manage_nicknames(self):
        self.value += 1 << 27
        return self

    @property
    def manage_roles(self):
        self.value += 1 << 28
        return self

    @property
    def manage_webhooks(self):
        self.value += 1 << 29
        return self

    @property
    def manage_emojis_and_stickers(self):
        self.value += 1 << 30
        return self

    @property
    def use_application_commands(self):
        self.value += 1 << 31
        return self

    @property
    def request_to_speak(self):
        self.value += 1 << 32
        return self

    @property
    def manage_events(self):
        self.value += 1 << 33
        return self

    @property
    def manage_threads(self):
        self.value += 1 << 34
        return self

    @property
    def create_public_threads(self):
        self.value += 1 << 35
        return self

    @property
    def create_private_threads(self):
        self.value += 1 << 36
        return self

    @property
    def use_external_stickers(self):
        self.value += 1 << 37
        return self

    @property
    def send_messages_in_threads(self):
        self.value += 1 << 38
        return self

    @property
    def start_embedded_activities(self):
        self.value += 1 << 39
        return self

    @property
    def moderator_members(self):
        self.value += 1 << 40
        return self

