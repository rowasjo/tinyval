from tempfile import TemporaryDirectory
from io import BytesIO
import pytest
from tinyval.adapters.repository import Repository
from tinyval.adapters.fsrepository import FilesystemRepository

EXAMPLE_1_KEY = "the-key"
EXAMPLE_1_VALUE = b"I am a little blob."
EXAMPLE_1_SIZE = 19


@pytest.fixture
def repository():
    with TemporaryDirectory() as data_dir:
        yield FilesystemRepository(data_dir=data_dir)


def test_get_path_returns_none_for_nonexistent_key(repository: Repository):
    assert repository.get_path(key="unknown key") is None


def test_get_size_returns_none_for_nonexistent_key(repository: Repository):
    assert repository.get_path(key="unknown key") is None


def test_set_and_get_file_happy_path(repository: Repository):
    with BytesIO(EXAMPLE_1_VALUE) as file:
        repository.set_from_stream(key=EXAMPLE_1_KEY, value=file)

    file_path = repository.get_path(key=EXAMPLE_1_KEY)
    assert file_path is not None

    with open(file_path, "rb") as repository_file:
        assert repository_file.read() == EXAMPLE_1_VALUE


def test_set_and_get_size_happy_path(repository: Repository):
    with BytesIO(EXAMPLE_1_VALUE) as file:
        repository.set_from_stream(key=EXAMPLE_1_KEY, value=file)

    assert repository.get_size(key=EXAMPLE_1_KEY) == EXAMPLE_1_SIZE
