import os
from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import PostgresDsn


BASE_DIR: Path = Path(__file__).resolve().parent.parent
# print(f"Settings path: {BASE_DIR}")


class AppSettings(BaseSettings):
    # # Paramètres de base
    # app_name: str = "mySite"
    # debug: bool = False
    # version: str = "1.0.0"

    # Configuration de la base de données
    database_url: PostgresDsn
    database_engine: str
    pghost: str
    database_port: int
    pguser: str
    pgpassword: str
    pgdatabase: str
    
    # Configuration du Blob Store
    blob_read_write_token: str

    # Configuration API ou autre
    # api_key: str

    class Config:
        env_file: str = ".env"
        env_file_encoding: str = "utf-8"
        # extra = "allow"
