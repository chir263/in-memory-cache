from cache import EvictionPolicyBase
from collections import OrderedDict, defaultdict
from typing import Any
import logging

class LFUEvictionPolicy(EvictionPolicyBase):
    def __init__(self):
        self.frequency = defaultdict(int)
        self.access_order = OrderedDict()

    def key_accessed(self, key: Any) -> None:
        if key in self.access_order:
            self.access_order.move_to_end(key)
        else:
            self.access_order[key] = None
        self.frequency[key] += 1

    def evict(self) -> Any:
        min_freq = float('inf')
        lfu_key = None

        for key, freq in self.frequency.items():
            if freq < min_freq:
                min_freq = freq
                lfu_key = key

        if lfu_key is None:
            logging.error("LFU eviction failed: no key found")
            return None

        del self.frequency[lfu_key]
        del self.access_order[lfu_key]

        return lfu_key