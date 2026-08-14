from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

# Getting .env file from where current folder is
BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str

    JWT_SECRET_KEY: str

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env"
    )

settings = Settings()