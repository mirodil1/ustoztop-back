import os
from logging import config as logging_config

from core.logger import LOGGING

logging_config.dictConfig(LOGGING)


PROJECT_NAME = os.environ.get("FAST_PROJECT_NAME", "statistics")
LANGUAGES = {
    "available": ["uz", "ru", "en"],
    "default": "uz",
}
# JWT_PUBLIC_KEY=open("public.pem").read()
JWT_ALGORITHM="RS256"
# Redis config
# REDIS_HOST = env("REDIS_HOST", "127.0.0.1")
# REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
