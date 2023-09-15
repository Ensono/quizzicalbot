from fastapi import FastAPI, Response, Request
from fastapi.openapi.models import Info
from fastapi.openapi.utils import get_openapi
from core.log_config import init_loggers, logger

# Include API versions and include in the API
from api_v1 import routes as api_v1_routes

init_loggers()

def custom_openapi():
    openapi_schema = get_openapi(
        title = "AI Question API",
        version = "0.0.1",
        description = "API to allow people to ask questions of own documents",
        routes = app.routes
    )
    return openapi_schema

app = FastAPI()

# Configure OpenAPI documentation
app.openapi = custom_openapi

# Include the routes from the different API versions
app.include_router(api_v1_routes.router, prefix="/api/v1")

# Create the logging middleware
# @app.middleware("http")
# async def api_logging(request: Request, call_next):
#     response = await call_next(request)

#     response_body = b""
#     async for chunk in response.body_iterator:
#         response_body += chunk

#     log_message = {
#         "host": request.url.hostname,
#         "endpoint": request.url.path,
#         "response": response_body.decode("utf-8"),
#     }

#     logger.debug(log_message)

#     return Response(
#         content = response_body,
#         status_code = response.status_code,
#         headers = dict(response.headers),
#         media_type=response.media_type
#     )
