from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    log_level: str
    openai_api_type: str
    openai_api_type: str
    openai_api_base: str
    openai_api_key: str
    openai_api_version: str
    azure_cognitive_search_service_name: str
    azure_cognitive_search_index_name: str
    azure_cognitive_search_api_key: str
    azure_cognitive_services_key: str
    azure_cognitive_services_endpoint: str
    storage_upload: str

settings = Settings()