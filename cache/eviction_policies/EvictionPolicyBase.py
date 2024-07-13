from abc import ABC, abstractmethod
from typing import Any, Optional

class EvictionPolicyBase(ABC):
    @abstractmethod
    def key_accessed(self, key: Any) -> None:
        pass

    @abstractmethod
    def evict(self) -> Any:
        pass
