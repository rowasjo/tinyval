from io import StringIO
from starlette.testclient import TestClient

UNKNOWN_BLOB_SHA256_HASH = (
    "61a04a46afa3c518551c887c6c1b2b1e4f25619fad3032c3d5c952849b2ff9db"
)

BLOB_EXAMPLE_1 = "I am a little blob."
BLOB_EXAMPLE_1_SHA256_HASH = (
    "bfb272e79d30466cf1af7c16739659e8b4e9b85b5075bdb922806c55035497cf"
)

BLOB_EXAMPLE_2 = "I am a little blob. I am growing."
BLOB_EXAMPLE_2_CHUNK = " I am growing."
BLOB_EXAMPLE_2_SHA256_HASH = (
    "cbbb84d2ec09a8e7f7a1e903393464bc6098498327c827cb3f0ac224f9300a29"
)


def test_get_blob_invalid_hash_returns_422_and_error_message(client: TestClient):
    response = client.get("/blobs/invalid-hash")
    assert response.status_code == 422
    assert response.json() == {"status": 422, "error": "Unprocessable Entity"}


def test_get_unknown_blob_returns_404_and_error_message(client: TestClient):
    response = client.get(f"/blobs/{UNKNOWN_BLOB_SHA256_HASH}")
    assert response.status_code == 404
    assert response.json() == {"status": 404, "error": "Not Found"}


def test_put_blob_with_invalid_body_returns_422_and_error_message(client: TestClient):
    response = client.put(f"/blobs/{UNKNOWN_BLOB_SHA256_HASH}", data="not a valid body")
    assert response.status_code == 422
    assert response.json() == {"status": 422, "error": "Unprocessable Entity"}


def test_put_blob_with_hash_mismatch_returns_422_and_error_message(
    client: TestClient,
):
    with StringIO(BLOB_EXAMPLE_1) as file:
        multipart_form_data = {"blob": file}
        response = client.put(
            f"/blobs/{UNKNOWN_BLOB_SHA256_HASH}", files=multipart_form_data
        )

    assert response.status_code == 422
    assert response.json() == {
        "status": 422,
        "error": "Unprocessable Entity",
        "detail": f"Uploaded blob has invalid SHA-256 hash: {BLOB_EXAMPLE_1_SHA256_HASH}",
    }


def test_put_blob_with_valid_hash_returns_200(client: TestClient):
    _put_example1_blob(client)


def test_get_uploaded_blob_happy_path(client: TestClient):
    _put_example1_blob(client)
    _get_example1_blob(client)


def test_head_uploaded_blob_happy_path(client: TestClient):
    _put_example1_blob(client)

    response = client.head(f"/blobs/{BLOB_EXAMPLE_1_SHA256_HASH}")
    assert response.status_code == 200
    assert response.headers["content-length"] == "19"
    assert response.text == ""


def _put_example1_blob(client: TestClient):
    with StringIO(BLOB_EXAMPLE_1) as file:
        multipart_form_data = {
            "blob": file,
        }
        response = client.put(
            f"/blobs/{BLOB_EXAMPLE_1_SHA256_HASH}", files=multipart_form_data
        )

    assert response.status_code == 200


def _get_example1_blob(client: TestClient):
    response = client.get(f"/blobs/{BLOB_EXAMPLE_1_SHA256_HASH}")
    assert response.status_code == 200
    assert response.text == BLOB_EXAMPLE_1
