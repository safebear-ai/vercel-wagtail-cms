import os
from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import Field

from pydantic import PostgresDsn


BASE_DIR: Path = Path(__file__).resolve().parent.parent
# print(f"Settings path: {BASE_DIR}")


class AppSettings(BaseSettings):
    # Paramètres de base
    app_name: str = "mysite"
    debug: bool = Field(..., env="DEBUG")
    version: str = "1.0.0"

    # Configuration de la base de données
    database_url: str = Field(..., env="DATABASE_URL")
    pghost: str = Field(..., env="PGHOST")
    pguser: str = Field(..., env="PGUSER")
    pgpassword: str = Field(..., env="PGPASSWORD")
    pgdatabase: str = Field(..., env="PGDATABASE")
    database_port: int = Field(..., env="DATABASE_PORT")
    database_engine: str = Field(..., env="DATABASE_ENGINE")
    
    # Configuration du Blob Store
    blob_read_write_token: str = Field(..., env="BLOB_READ_WRITE_TOKEN")

    class Config:
        # Charger le fichier .env en fonction de la variable ENVIRONMENT
        env_file: str = f".env.{os.getenv('ENVIRONMENT', 'development')}"
        env_file_encoding: str = "utf-8"
