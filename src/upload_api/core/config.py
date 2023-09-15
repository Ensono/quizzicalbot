from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    log_level: str
    upload_dir: str
    azure_storage_connection_string: str
    azure_storage_container: str

settings = Settings()