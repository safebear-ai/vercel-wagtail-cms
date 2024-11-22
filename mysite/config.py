import os
from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn



BASE_DIR: Path = Path(__file__).resolve().parent.parent
print(BASE_DIR)
print(f".env.{os.getenv('ENVIRONMENT', 'local')}")

class AppSettings(BaseSettings):
    # # Paramètres de base
    app_name: str = "mysite"
    debug: bool
    version: str = "1.0.0"

    # Configuration de la base de données
    
    database_url: str
    pghost: str
    pguser: str
    pgpassword: str
    pgdatabase: str
    database_port: int
    database_engine: str = "django.db.backends.postgresql"
    
    # Configuration du Blob Store
    blob_read_write_token: str

    # Configuration API ou autre
    # api_key: str

    class Config:
        env_file: str = f".env.{os.getenv('ENVIRONMENT', 'production')}"
        # env_file: str = f".env.{os.getenv('ENVIRONMENT', 'local')}"
        env_file_encoding: str = "utf-8"

