from abc import ABCMeta, abstractmethod
from typing import BinaryIO, List


class BaseStore(metaclass=ABCMeta):
    @abstractmethod
    def init(self) -> None:
        ...

    @abstractmethod
    def object_exists(self, path: str) -> None:
        ...

    @abstractmethod
    def upload_object(self, content: BinaryIO, path: str) -> None:
        ...

    @abstractmethod
    def download_object(self, path: str) -> bytes:
        ...

    @abstractmethod
    def list_objects(self, path: str) -> List[str]:
        ...

    @abstractmethod
    def list_basename(self, path: str) -> List[str]:
        ...
