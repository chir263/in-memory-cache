from pydantic import BaseModel

from .eviction_policies import FIFOEvictionPolicy, EvictionPolicyBase, LRUEvictionPolicy, LIFOEvictionPolicy

from .InMemoryCache import InMemoryCache

class EvictionPolicy():
    FIFO = FIFOEvictionPolicy
    LRU = LRUEvictionPolicy
    LIFO = LIFOEvictionPolicy
