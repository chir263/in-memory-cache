from cache import InMemoryCache, EvictionPolicy
from time import sleep

cache = InMemoryCache(capacity=3, eviction_policy=EvictionPolicy.LRU, ttl=5)

cache.put("key1", "value1")
cache.put("key2", "value2")
cache.put("key3", "value3")
cache.get("key1")
cache.put("key4", "value4")

print(cache.get("key1")) 
print(cache.get("key2")) 
print(cache.get("key3")) 
print(cache.get("key4"))


sleep(5)

print("After 5 seconds")

print(cache.get("key1")) 
print(cache.get("key2")) 
print(cache.get("key3")) 
print(cache.get("key4"))
