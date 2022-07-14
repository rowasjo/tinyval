import os
from starlette.requests import Request
from starlette.responses import HTMLResponse, PlainTextResponse
from starlette.routing import Route


OPENAPI_YAML_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "openapi.yaml")
)
OPENAPI_YAML_URL = "/openapi.yaml"


def openapi_spec_route():
    with open(OPENAPI_YAML_PATH, mode="rt", encoding="utf-8") as file:
        openapi_yaml = file.read()

    async def get_openapi_yaml_spec(_: Request) -> PlainTextResponse:
        return PlainTextResponse(openapi_yaml)

    return Route(path=OPENAPI_YAML_URL, endpoint=get_openapi_yaml_spec, methods=["GET"])


def openapi_docs_route():

    html = get_swagger_ui_html(OPENAPI_YAML_URL)

    async def get_openapi_docs(_: Request) -> HTMLResponse:
        return HTMLResponse(html)

    return Route(path="/docs", endpoint=get_openapi_docs, methods=["GET"])


def get_swagger_ui_html(url: str) -> str:

    # We embed Swagger UI's code directly in HTML by using unpkg's interface.
    # For documentation see:
    #   https://swagger.io/docs/open-source-tools/swagger-ui/usage/installation/

    html = f"""<!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="utf-8" />
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <meta name="description" content="SwaggerUI" />
      <title>Tinyval - Swagger UI</title>
      <link type="text/css" rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@4.5.0/swagger-ui.css" />
    </head>
    <body>
    <div id="swagger-ui"></div>
    <script src="https://unpkg.com/swagger-ui-dist@4.5.0/swagger-ui-bundle.js" crossorigin></script>
    <script>
      window.onload = () => {{
        window.ui = SwaggerUIBundle({{
          url: '{url}',
          dom_id: '#swagger-ui',
          layout: "BaseLayout",
          deepLinking: true,
          displayRequestDuration: true,
          showExtensions: true,
          showCommonExtensions: true,
          presets: [
            SwaggerUIBundle.presets.apis,
            SwaggerUIBundle.SwaggerUIStandalonePreset
          ],
        }});
      }};
    </script>
    </body>
    </html>"""

    return html
