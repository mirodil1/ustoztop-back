import os
from logging import config as logging_config

from pydantic_settings import BaseSettings

from core.logger import LOGGING

logging_config.dictConfig(LOGGING)


class Settings(BaseSettings):
    project_name: str = os.environ.get("FAST_PROJECT_NAME", "announcements")
    languages: dict = {
        "available": ["uz", "ru", "en"],
        "default": "uz",
    }
    jwt_public_key: str = open("public.pem").read()
    jwt_algorithm: str = "RS256"

    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    base_url: str = os.environ.get("FAST_BASE_URL", "http://localhost:8000")
    stat_url: str = os.environ.get("FAST_STAT_URL")
    user_url: str = os.environ.get("FAST_USER_URL")

    origins: list = [
        origin.strip() for origin in os.environ.get(
            "FAST_ORIGINS", "http://localhost:3000"
        ).split(",")
    ]
    debug: bool = os.environ.get("FAST_DEBUG", "True") == "True"

settings = Settings()
