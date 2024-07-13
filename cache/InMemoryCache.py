import time
from threading import RLock, Thread
from typing import Any, Optional
from .BaseCache import BaseCache   
from . import EvictionPolicyBase
from .eviction_policies import LRUEvictionPolicy

class InMemoryCache(BaseCache):


    def __init__(self, capacity: int = 100, eviction_policy: EvictionPolicyBase = LRUEvictionPolicy, ttl: Optional[int] = None):
        
        if ttl and ttl <= 0:
            raise ValueError("TTL should be None or a positive integer")
        if capacity <= 0:
            raise ValueError("Capacity should be a positive integer")
        
        self.capacity = capacity
        self.eviction_policy = eviction_policy()
        self.ttl = ttl
        self.cache = {}
        self.timestamps = {}
        self.lock = RLock()
        if ttl:
            Thread(target=self.__start_ttl_cleaner, daemon=True).start()

    def __start_ttl_cleaner(self):
        while True:
            time.sleep(self.ttl)
            self.__remove_expired_items()

    def __remove_expired_items(self):
        with self.lock:
            current_time = time.time()
            keys_to_remove = [key for key, timestamp in self.timestamps.items()
                              if current_time - timestamp >= self.ttl]
            for key in keys_to_remove:
                self.cache.pop(key, None)
                self.timestamps.pop(key, None)

    def get(self, key: Any) -> Optional[Any]:
        with self.lock:
            if key in self.cache:
                if self.ttl and time.time() - self.timestamps[key] >= self.ttl:
                    self.cache.pop(key, None)
                    self.timestamps.pop(key, None)
                    return None
                self.eviction_policy.key_accessed(key)
                self.timestamps[key] = time.time()
                return self.cache[key]
            return None

    def put(self, key: Any, value: Any) -> None:
        with self.lock:
            if key not in self.cache and len(self.cache) >= self.capacity:
                evicted_key = self.eviction_policy.evict()
                self.cache.pop(evicted_key, None)
                self.timestamps.pop(evicted_key, None)
            self.cache[key] = value
            self.eviction_policy.key_accessed(key)
            self.timestamps[key] = time.time()

    def remove(self, key: Any) -> None:
        with self.lock:
            if key in self.cache:
                del self.cache[key]
                del self.timestamps[key]

    def clear(self) -> None:
        with self.lock:
            self.cache.clear()
            self.timestamps.clear()
