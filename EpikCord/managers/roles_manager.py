from .cache_manager import CacheManager
class RoleManager(CacheManager):
    def __init__(self, limit=1000):
        super().__init__(limit)