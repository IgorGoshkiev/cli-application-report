from abc import ABC, abstractmethod
from typing import Dict, Optional


class BaseLogParser(ABC):
    @abstractmethod
    def can_parse(self, message: str) -> bool:
        pass

    @abstractmethod
    def parse(self, message: str) -> Optional[Dict[str, str]]:
        pass
