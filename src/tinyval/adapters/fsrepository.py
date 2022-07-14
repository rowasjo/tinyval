import os.path
import shutil
from typing import BinaryIO
from tinyval.adapters.repository import Repository


class FilesystemRepository:
    """Basic filesystem-based implementation of the Repository protocol"""

    def __init__(self, data_dir):
        self.data_dir = data_dir

    def __contains__(self, key: str) -> bool:
        return os.path.isfile(self._blob_path(key))

    def set_from_stream(self, key: str, value: BinaryIO):
        # TODO: This implementation is not atomic.
        # It may leave behind an invalid file if an error occurs.
        with open(self._blob_path(key), "wb") as new_file:
            shutil.copyfileobj(value, new_file)

    def get_path(self, key: str) -> str | None:
        path = self._blob_path(key)
        if os.path.isfile(path):
            return path

        return None

    def get_size(self, key: str) -> int | None:
        path = self._blob_path(key)
        if os.path.isfile(path):
            return os.path.getsize(self._blob_path(key))

        return None

    def _blob_path(self, key: str) -> str:
        return os.path.join(self.data_dir, key)


assert issubclass(FilesystemRepository, Repository)
