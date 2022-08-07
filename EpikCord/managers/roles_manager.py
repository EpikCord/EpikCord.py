from .cache_manager import CacheManager
class RoleManager(CacheManager):
    def __init__(self, client, limit=1000):
        super().__init__(limit)