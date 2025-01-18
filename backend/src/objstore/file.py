from pathlib import Path
from typing import BinaryIO, List

from src.objstore.base import BaseStore


class FileStore(BaseStore):
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.init()

    def init(self) -> None:
        """Ensure the base directory exists."""
        self.base_path.mkdir(parents=True, exist_ok=True)

    def object_exists(self, path: str) -> bool:
        """Check if a file or directory exists."""
        return (self.base_path / path).exists()

    def upload_object(self, content: BinaryIO, path: str) -> None:
        """Write content to a file."""
        target_path = self.base_path / path
        target_path.parent.mkdir(parents=True, exist_ok=True)
        with target_path.open(mode="wb") as file:
            file.write(content.read())

    def download_object(self, path: str) -> bytes:
        """Read and return content of a file."""
        target_path = self.base_path / path
        if not target_path.exists():
            raise FileNotFoundError(f"The path {path} does not exist.")
        return target_path.read_bytes()

    def list_objects(self, path: str) -> List[str]:
        """List all files and directories under a given path."""
        target_path = self.base_path / path
        if not target_path.is_dir():
            raise NotADirectoryError(f"The path {path} is not a directory.")
        return [str(p.relative_to(self.base_path)) for p in target_path.rglob("*")]

    def list_basename(self, path: str) -> List[str]:
        """List basenames of all files and directories under a given path."""
        target_path = self.base_path / path
        if not target_path.is_dir():
            raise NotADirectoryError(f"The path {path} is not a directory.")
        return [p.name for p in target_path.iterdir()]
