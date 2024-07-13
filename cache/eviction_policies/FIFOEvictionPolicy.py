from collections import deque
from typing import Any
from .EvictionPolicyBase import EvictionPolicyBase
import logging

class FIFOEvictionPolicy(EvictionPolicyBase):
    def __init__(self):
        self.queue = deque()
        self.keys_set = set()

    def key_accessed(self, key: Any) -> None:
        if key not in self.keys_set:
            self.queue.append(key)
            self.keys_set.add(key)

    def evict(self) -> Any:
        if len(self.queue) == 0:
            logging.error("Queue is empty")
            return None
        evicted_key = self.queue.popleft()
        self.keys_set.remove(evicted_key)
        logging.info(f"Evicting {evicted_key}")
        return evicted_key
