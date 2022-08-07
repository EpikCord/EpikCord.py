from .cache_manager import CacheManager
class RoleManager(CacheManager):
    def __init__(self, client, limit=5000):
        super().__init__(limit)