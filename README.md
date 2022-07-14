# Tinyval

Hash table service for storing and retrieving values (blobs) using their SHA-256 hashes as keys.

This service could be deployed as many single-node instances each using own local storage (e.g. a filesystem).
Responsibilities involving high availability, partitioning, per-value authorization, and anything metadata related are delegated to other services.
The idea is to let this service be a general-purpose component used to build distributed hash table (DHT) based systems.

Note that this is primarily an experiment in using Python to develop HTTP services.

## Development

### Setup

Setup will create a virtual environment in which to:
1. install build tools
2. install project in development mode
3. install uvicorn as the ASGI server.

```
cd <source-dir>
python3 -m venv .venv
. .venv/bin/activate
pip install --upgrade pip wheel build setuptools
pip install -e ".[dev]"
pip install uvicorn
```

After installing dependencies reactivate the environment to ensure the virtual environment is used for pytest and uvicorn commands:
```
. .venv/bin/activate
```

### Run Tests

```
pytest tests/unit
pytest tests/e2e
```

### Deploy

To deploy you must create a .env file and set environment variables.

```
TINYVAL_DEBUG=True
TINYVAL_DATA_DIR=<data-dir>
```

Deploy the app with uvicorn using the create_app factory function:

```
uvicorn --factory tinyval.api:create_app --reload
```

Uvicorn should serve the API at http://127.0.0.1:8000, so you should be able to access Tinyval's interactive OpenAPI HTML interface at http://127.0.0.1:8000/docs.

### Package

```
python3 -m build
```

## Notable Technical Details

- The HTTP implementation is based on the Starlette ASGI-based web framework.
- The HTTP API is described by the OpenAPI schema [src/tinyval/openapi.yaml](src/tinyval/openapi.yaml).
- Swagger UI is used to provide a HTML page endpoint, '/docs', to visualize and interact with the API's resources.
