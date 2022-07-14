from typing import Protocol, BinaryIO, runtime_checkable


@runtime_checkable
class Repository(Protocol):
    """Protocol for storing and retrieving file-like values using strings as keys"""

    # TODO: These methods should probably be async.

    def __contains__(self, key: str) -> bool:
        """Check if value exists"""

    def set_from_stream(self, key: str, value: BinaryIO):
        """Set value contents from stream"""

    def get_path(self, key: str) -> str | None:
        """Get file path with the value contents"""
        # We're using file path due to Starlette limitations.
        # Returning a file-like object with known content length would be preferable.

    def get_size(self, key: str) -> int | None:
        """Get size (bytes) of value"""
