from typing import Optional

class SystemChannelFlags:
    def __init__(self, *, value: Optional[int] = None):
        self.value: int = value

    @property
    def suppress_join_notifications(self):
        self.value += 1 << 0
    
    @property
    def suppress_premium_subscriptions(self):
        self.value += 1 << 1
    
    @property
    def suppress_guild_reminder_notifications(self):
        self.value += 1 << 2

    @property
    def supporess_join_notification_replies(self):
        self.value += 1 << 3
