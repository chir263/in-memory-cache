from collections import OrderedDict
from typing import Any
from .EvictionPolicyBase import EvictionPolicyBase
import logging

class LRUEvictionPolicy(EvictionPolicyBase):
    def __init__(self):
        self.order = OrderedDict()

    def key_accessed(self, key: Any) -> None:
        if key in self.order:
            self.order.move_to_end(key)
        else:
            self.order[key] = None

    def evict(self) -> Any:
        evicted_key, _ = self.order.popitem(last=False)
        logging.info(f"Evicting {evicted_key}")
        return evicted_key
