from abc import ABCMeta, abstractmethod
from typing import List

from src.entities import Metric


class ValidationInterface(metaclass=ABCMeta):
    @abstractmethod
    def validate(self) -> List[Metric]:
        ...
