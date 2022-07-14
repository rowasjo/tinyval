from starlette.requests import Request
from starlette.responses import FileResponse, Response
from starlette.exceptions import HTTPException
from starlette import status
from starlette.routing import Route

from tinyval.adapters.repository import Repository
from tinyval.hashutil import hash_file, is_valid_sha256_hash


def get_blob_route(repository: Repository):
    async def get_blob(request: Request):
        sha256_hash = request.path_params["hash"]

        if not is_valid_sha256_hash(sha256_hash):
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY)

        if sha256_hash not in repository:
            raise HTTPException(status.HTTP_404_NOT_FOUND)

        if request.method == "HEAD":
            return Response(
                headers={"content-length": f"{repository.get_size(sha256_hash)}"}
            )

        # Use of file response assumes that content is a file on disk.
        # StreamingResponse accepts a file-like object which is more flexible,
        # but it only supports chunked encoding response which we don't want.
        return FileResponse(
            path=repository.get_path(sha256_hash),
            headers={"Cache-Control": "max-age=31536000, immutable"},
        )

    return Route(path="/blobs/{hash:str}", endpoint=get_blob, methods=["GET", "HEAD"])


def put_blob_route(repository: Repository):
    async def put_blob(request: Request):
        sha256_hash = request.path_params["hash"]

        if not is_valid_sha256_hash(sha256_hash):
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY)

        form = await request.form()

        if "blob" not in form:
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY)

        blob_file = form["blob"].file

        # TODO: computing hash should either be async or be delegated to a separate thread.
        blob_hash = hash_file(blob_file).hexdigest()
        if blob_hash != sha256_hash:
            raise HTTPException(
                status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Uploaded blob has invalid SHA-256 hash: {blob_hash}",
            )

        if sha256_hash not in repository:
            repository.set_from_stream(sha256_hash, blob_file)

        return Response(status_code=200)

    return Route(path="/blobs/{hash:str}", endpoint=put_blob, methods=["PUT"])
