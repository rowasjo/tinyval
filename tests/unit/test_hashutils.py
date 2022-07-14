from io import BytesIO
from tinyval.hashutil import hash_file, is_valid_sha256_hash

BLOB_EXAMPLE_1 = b"I am a little blob."
BLOB_EXAMPLE_1_SHA256_HASH = (
    "bfb272e79d30466cf1af7c16739659e8b4e9b85b5075bdb922806c55035497cf"
)


def test_sha256_regex_matches_valid_value():
    assert is_valid_sha256_hash(
        "d0b147f4164bce77e71a28d191f462ba7b7adf4912da6edb24a6cbe6cc9e56cc"
    )


def test_sha256_regex_too_short():
    assert not is_valid_sha256_hash(
        "d0b147f4164bce77e71a28d191f462ba7b7adf4912da6edb24a6cbe6cc9e56c"
    )


def test_sha256_regex_too_long():
    assert not is_valid_sha256_hash(
        "d0b147f4164bce77e71a28d191f462ba7b7adf4912da6edb24a6cbe6cc9e56ccc"
    )


def test_sha256_regex_illegal_char():
    assert not is_valid_sha256_hash(
        "d0b147f4164bce77e71a28d191f462ba7b7adf_912da6edb24a6cbe6cc9e56cc"
    )


def test_hash_file():
    with BytesIO(BLOB_EXAMPLE_1) as file:
        assert hash_file(file).hexdigest() == BLOB_EXAMPLE_1_SHA256_HASH
