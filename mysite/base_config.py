import os
from pathlib import Path
from pydantic_settings import BaseSettings


BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
print(f"Settings path: {BASE_DIR}")


class AppSettings(BaseSettings):
    # Paramètres de base
    app_name: str = "mySite"
    debug: bool = False
    version: str = "1.0.0"

    # Configuration de la base de données
    db_engine: str
    db_host: str
    db_port: int
    db_user: str
    db_password: str
    db_name: str

    # Configuration API ou autre
    # api_key: str

    class Config:
        env_file = ".env"  # Spécifie le fichier contenant les variables d’environnement
        env_file_encoding = "utf-8"
