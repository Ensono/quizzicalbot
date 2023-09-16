from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    log_level: str
    storage_upload: str
    azure_storage_connection_string: str
    azure_storage_container: str
    api_key: str

settings = Settings()