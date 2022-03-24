class CacheManager:
    def __init__(self, cache_key: str = "cache"):
        self.cache_key: str = cache_key
        setattr(self, cache_key, []) # Dynamic for subclasses
    
    def add_to_cache(self, key, value):
        getattr(self, self.cache_key)[key] = value
    
    def remove_from_cache(self, key):
        getattr(self, self.cache_key).pop(key, None)
        
    def get_from_cache(self, key):
        return getattr(self, self.cache_key).get(key, None)

    def is_in_cache(self, key):
        return key in getattr(self, self.cache_key)
    
    def clear_cache(self):
        setattr(self, self.cache_key, {})
    
    def __dict__(self):
        return getattr(self, self.cache_key)
    
    def __str__(self):
        return f"<CacheManager cache={getattr(self, self.cache_key)}>"

    def __int__(self):
        return len(getattr(self, self.cache_key))
    
    def __len__(self):
        return len(getattr(self, self.cache_key))
    
    def __repr__(self):
        return self.__str__()
    
    def __getitem__(self, key):
        return getattr(self, self.cache_key)[key]
    
    def __setitem__(self, key, value):
        getattr(self, self.cache_key)[key] = value
    
    def __delitem__(self, key):
        getattr(self, self.cache_key).pop(key, None)
    
    def __contains__(self, key):
        return key in getattr(self, self.cache_key)
    
    def __iter__(self):
        return iter(getattr(self, self.cache_key))
    
    def __next__(self):
        return next(getattr(self, self.cache_key))
    
    def __eq__(self, other):
        return getattr(self, self.cache_key) == other.cache
    
    def __ne__(self, other):
        return getattr(self, self.cache_key) != other.cache
    
    def __gt__(self, other):
        return getattr(self, self.cache_key) > other.cache
    
    def __ge__(self, other):
        return getattr(self, self.cache_key) >= other.cache
    
    def __lt__(self, other):
        return getattr(self, self.cache_key) < other.cache
    
    def __le__(self, other):
        return getattr(self, self.cache_key) <= other.cache
    
    def __hash__(self):
        return hash(getattr(self, self.cache_key))
    
    def __call__(self):
        return getattr(self, self.cache_key)
    
# This is the base cache manager, people can extend this to make their own cache managers