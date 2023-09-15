from fastapi import FastAPI, Response
from fastapi.openapi.utils import get_openapi
from core.log_config import init_loggers, logger

# Import routes
from api_v1 import routes as api_v1_routes

# Initialise the FastAPI app
init_loggers()

def custom_openapi():
    openapi_schema = get_openapi(
        title = "Document Uploader API",
        version = "0.0.1",
        description = "API to allow the upload of documents to Azure Blob storage so that they can be indexed for AI question bot",
        routes = app.routes
    )
    return openapi_schema

app = FastAPI()

# Configure OpenAPI documentation
app.openapi = custom_openapi

# Include the routes from the different API versions
app.include_router(api_v1_routes.router, prefix="/api/v1")
