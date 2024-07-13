from typing import Any
from .EvictionPolicyBase import EvictionPolicyBase
import logging

class LIFOEvictionPolicy(EvictionPolicyBase):
    def __init__(self):
        self.stack = []
        self.position_dict = {}

    def key_accessed(self, key: Any) -> None:
        if key not in self.position_dict:
            self.stack.append(key)
            self.position_dict[key] = len(self.stack) - 1

    def evict(self) -> Any:
        evicted_key = self.stack.pop()
        logging.info(f"Evicting {evicted_key}")
        del self.position_dict[evicted_key]
        return evicted_key
