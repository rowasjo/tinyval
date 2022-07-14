import http
from pathlib import Path
from starlette.requests import Request
from starlette.exceptions import HTTPException
from starlette.responses import JSONResponse
from starlette.config import Config
from starlette.applications import Starlette
from tinyval.entrypoints import storage, openapi
from tinyval.adapters.fsrepository import FilesystemRepository
from tinyval import settings


def create_app(config: Config = Config(env_file=".env")):
    debug = config(settings.DEBUG_KEY, cast=bool, default=False)
    data_dir = config(settings.DATA_DIR_KEY, cast=Path)

    repository = FilesystemRepository(data_dir)

    return Starlette(
        debug=debug,
        routes=[
            storage.get_blob_route(repository),
            storage.put_blob_route(repository),
            openapi.openapi_spec_route(),
            openapi.openapi_docs_route(),
        ],
        exception_handlers={HTTPException: http_exception},
    )


async def http_exception(_: Request, exc: HTTPException):

    error = http.HTTPStatus(exc.status_code).phrase

    body = {"status": exc.status_code, "error": error}

    if exc.detail != error:
        body["detail"] = exc.detail

    return JSONResponse(body, status_code=exc.status_code)
