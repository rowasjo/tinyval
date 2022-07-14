from starlette.testclient import TestClient


def test_get_openapi_yaml(client: TestClient):
    response = client.get("/openapi.yaml")
    assert response.status_code == 200


def test_get_openapi_docs(client: TestClient):
    response = client.get("/docs")
    assert response.status_code == 200
