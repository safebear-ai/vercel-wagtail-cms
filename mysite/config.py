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

    # Database configuration variables
    database_url: str
    database_url_unpooled: str = ""
    pghost: str
    pghost_unpooled: str
    pgdatabase: str
    pgpassword: str
    pguser: str
    postgres_database: str
    postgres_host: str
    postgres_password: str
    postgres_prisma_url: str
    postgres_url: str
    postgres_url_non_pooling: str
    postgres_url_no_ssl: str
    postgres_user: str
    
    database_port: int = 5432
    database_engine: str = "django.db.backends.postgresql"
    
    # BlobStore configuration
    blob_read_write_token: str

    # API
    blob_bucket: str = "gqb3dhg6ajkwelj6"
    blob_base_url: str = f"https://{blob_bucket}.public.blob.vercel-storage.com"
    

    class Config:
        env_file: str = f".env.{os.getenv('ENVIRONMENT', "local")}"
        env_file_encoding: str = "utf-8"
        print(f"Chargement des paramètres depuis le fichier {env_file}")
        