import os
from pathlib import Path
from pydantic_settings import BaseSettings

BASE_DIR: Path = Path(__file__).resolve().parent.parent

class AppSettings(BaseSettings):
    # # Paramètres de base
    app_name: str = "mysite"
    debug: bool
    version: str = "1.0.0"
    environment: str

    # Configuration de la base de données
    database_url: str
    pghost: str
    pguser: str
    pgpassword: str
    pgdatabase: str
    database_port: int = 5432
    database_engine: str = "django.db.backends.postgresql"
    
    # Configuration du Blob Store
    blob_read_write_token: str
    blob_bucket: str

    # Configuration API ou autre
    api_base_url: str = "https://blob.vercel-storage.com"

    class Config:
        env_file: str = f".env.{os.getenv('ENVIRONMENT', 'development')}"
        env_file_encoding: str = "utf-8"
        print(f"Chargement des paramètres depuis le fichier {env_file}")