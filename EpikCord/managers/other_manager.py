from functools import cache
from .cache_manager import CacheManager 

class AutoModerationRuleManager(CacheManager):
    def __init__(self, limit=1000):
        super().__init__(limit)


class ScheduledEventManager(CacheManager):
    def __init__(self, client, limit=1000):
        super().__init__(limit)
        
