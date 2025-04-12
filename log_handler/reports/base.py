from abc import ABC, abstractmethod
from typing import List, Dict, TypeVar, Type

T = TypeVar('T', bound='BaseReport')


class BaseReport(ABC):
    name: str  # Теперь это атрибут класса, а не property

    @classmethod
    @abstractmethod
    def generate(cls: Type[T], records: List[Dict[str, str]]) -> str:
        """Абстрактный метод для генерации отчета"""
        pass