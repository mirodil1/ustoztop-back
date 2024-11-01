import os
from logging import config as logging_config

from pydantic_settings import BaseSettings

from core.logger import LOGGING

logging_config.dictConfig(LOGGING)


class Settings(BaseSettings):
    project_name: str = os.environ.get("FAST_PROJECT_NAME", "statistics")
    languages: dict = {
        "available": ["uz", "ru", "en"],
        "default": "uz",
    }
    jwt_algorithm: str = "RS256"
    jwt_public_key: str = open("public.pem").read()

    mongodb_url: str = os.getenv("MONGODB_URL", "mongodb://statistics_mongo:27017")
    mongodb_db: str = os.getenv("MONGODB_DB", "statistics")

    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    debug: bool = os.getenv("DEBUG", "True") == "True"

settings = Settings()
