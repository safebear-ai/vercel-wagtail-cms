import os
from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn
from dotenv import load_dotenv


load_dotenv()

BASE_DIR: Path = Path(__file__).resolve().parent.parent

class AppSettings(BaseSettings):
    # # Paramètres de base
    app_name: str = "mysite"
    debug: bool
    version: str = "1.0.0"
    environment: str

    # Configuration de la base de données
    database_url: str
    # database_url_unpooled: str
    pghost: str
    # pghost_unpooled: str
    pguser: str
    pgpassword: str
    pgdatabase: str
    database_port: int = 5432
    database_engine: str = "django.db.backends.postgresql"
    
    # Configuration du Blob Store
    blob_read_write_token: str

    # Configuration API ou autre
    # api_key: str

    class Config:
        env_file: str = f".env.{os.getenv('ENVIRONMENT', 'development')}"
        env_file_encoding: str = "utf-8"