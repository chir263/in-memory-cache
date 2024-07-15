from cache import EvictionPolicyBase
from collections import defaultdict, OrderedDict
from typing import Any
import logging

class LFUEvictionPolicy(EvictionPolicyBase):
    def __init__(self):
        self.frequency = defaultdict(int)
        self.keys_by_frequency = defaultdict(OrderedDict)
        self.min_frequency = 0

    def key_accessed(self, key: Any) -> None:
        
        if key in self.frequency:
            freq = self.frequency[key]
            del self.keys_by_frequency[freq][key]
            if not self.keys_by_frequency[freq]:
                del self.keys_by_frequency[freq]
                if self.min_frequency == freq:
                    self.min_frequency += 1
            self.frequency[key] += 1
            freq = self.frequency[key]
        else:
            self.frequency[key] = 1
            freq = 1
            self.min_frequency = 1

        self.keys_by_frequency[freq][key] = None

    def evict(self) -> Any:
        if not self.keys_by_frequency:
            logging.error("LFU eviction failed: no key found")
            return None

        lfu_key, _ = self.keys_by_frequency[self.min_frequency].popitem(last=False)
        if not self.keys_by_frequency[self.min_frequency]:
            del self.keys_by_frequency[self.min_frequency]
            self.min_frequency += 1

        del self.frequency[lfu_key]
        return lfu_key
