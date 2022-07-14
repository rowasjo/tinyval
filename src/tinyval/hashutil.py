import re
import hashlib
from typing import BinaryIO

# SHA-256 regex, matches any 64 char hexadecimal (lowercase)
SHA256_HEX_REGEX: str = "^[0-9a-f]{64}$"
BLOCKSIZE = 65536


def hash_file(file: BinaryIO):
    """Compute SHA-256 hash of file-like object"""
    pos = file.tell()
    try:
        hasher = hashlib.sha256()
        buf = file.read(BLOCKSIZE)
        while buf:
            hasher.update(buf)
            buf = file.read(BLOCKSIZE)
        return hasher
    finally:
        file.seek(pos)


def is_valid_sha256_hash(sha256_hash: str) -> bool:
    return re.compile(SHA256_HEX_REGEX).match(sha256_hash)
