from abc import ABC, abstractmethod
from typing import Any, Optional

class BaseCache(ABC):

    @abstractmethod
    def get(self, key: Any) -> Optional[Any]:
        pass

    @abstractmethod
    def put(self, key: Any, value: Any) -> None:
        pass

    @abstractmethod
    def remove(self, key: Any) -> None:
        pass

    @abstractmethod
    def clear(self) -> None:
        pass
