import tempfile
import pytest
from starlette.applications import Starlette
from starlette.config import Environ, Config
from starlette.testclient import TestClient
from tinyval import api


@pytest.fixture()
def app() -> Starlette:
    with tempfile.TemporaryDirectory() as tmpdir:
        environ = Environ({api.DATA_DIR_KEY: tmpdir, api.DEBUG_KEY: True})
        yield api.create_app(config=Config(environ=environ))


@pytest.fixture()
def client(app) -> TestClient:
    return TestClient(app)
