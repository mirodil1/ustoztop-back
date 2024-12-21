import os
import random
import string
from datetime import timedelta

jwt_access_token_expires_days = int(os.environ.get("JWT_ACCESS_TOKEN_EXPIRES_MINUTES")) if \
    os.environ.get("JWT_ACCESS_TOKEN_EXPIRES_MINUTES") else 31

jwt_refresh_token_expires_days = int(os.environ.get("JWT_REFRESH_TOKEN_EXPIRES_DAYS")) if \
    os.environ.get("JWT_REFRESH_TOKEN_EXPIRES_DAYS") else 60


class Config:

    basedir = os.path.abspath(os.path.dirname(__file__))
    BASE_URL = os.environ.get("BASE_URL", "http://localhost:5000")

    # Assets Management ================================================================
    ASSETS_ROOT = os.getenv("ASSETS_ROOT", "/static/assets")

    # Set up the App SECRET_KEY ========================================================
    SECRET_KEY  = os.getenv("SECRET_KEY", None)
    if not SECRET_KEY:
        SECRET_KEY = "".join(random.choice(string.ascii_lowercase) for i in range( 32 ))

    # JWT config =======================================================================
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=jwt_access_token_expires_days)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=jwt_refresh_token_expires_days)
    JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM", "RS256")
    JWT_PUBLIC_KEY = open("public.pem").read()
    JWT_PRIVATE_KEY = open("private.pem").read()

    # Redis ============================================================================
    REDIS_HOST = os.environ.get("REDIS_HOST", "redis")
    REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))

    # Media upload =====================================================================
    UPLOAD_FOLDER = "./src/media/uploads"
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
    MAX_CONTENT_LENGTH = 10 * 1000 * 1000

    # Services url =====================================================================
    STATISTICS_URL = os.environ.get("STATISTICS_URL")
    ANNOUNCEMENTS_URL = os.environ.get("ANNOUNCEMENTS_URL")

    # Eskiz ============================================================================
    ESKIZ_EMAIL = os.environ.get("ESKIZ_EMAIL")
    ESKIZ_PASSWORD = os.environ.get("ESKIZ_PASSWORD")

    # Payme ============================================================================
    PAYME_MIN_AMOUNT = os.environ.get("PAYME_MIN_AMOUNT")
    PAYME_SECRET_KEY = os.environ.get("PAYME_SECRET_KEY")
    PAYME_TRANSACTION_TIMEOUT = os.environ.get("PAYME_TRANSACTION_TIMEOUT")
    PAYME_MERCHANT_ID = os.environ.get("PAYME_MERCHANT_ID")

    # Click ============================================================================
    CLICK_MIN_AMOUNT = os.environ.get("CLICK_MIN_AMOUNT")
    CLICK_SECRET_KEY = os.environ.get("CLICK_SECRET_KEY")
    CLICK_MERCHANT_ID = os.environ.get("CLICK_MERCHANT_ID")
    CLICK_SERVICE_ID = os.environ.get("CLICK_SERVICE_ID")
    CLICK_MERCHANT_USER_ID = os.environ.get("CLICK_MERCHANT_USER_ID")

    # Database configs =================================================================
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    POSTGRES_ENGINE   = os.getenv("POSTGRES_ENGINE"   , None)
    POSTGRES_USER     = os.getenv("POSTGRES_USER" , None)
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD"     , None)
    POSTGRES_HOST     = os.getenv("POSTGRES_HOST"     , None)
    POSTGRES_PORT     = os.getenv("POSTGRES_PORT"     , None)
    POSTGRES_DB       = os.getenv("POSTGRES_DB"     , None)

    # try to set up a Relational DBMS
    if POSTGRES_ENGINE and POSTGRES_DB and POSTGRES_USER:
        try:
            # Relational DBMS: PSQL, MySql
            SQLALCHEMY_DATABASE_URI = f"{POSTGRES_ENGINE}://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
        except Exception as e:
            print("> Error: DBMS Exception: " + str(e) )


class ProductionConfig(Config):
    DEBUG = False

    # Security
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_DURATION = 3600


class LocalConfig(Config):
    DEBUG = True


# Load all possible configurations
config_dict = {
    "Production": ProductionConfig,
    "Local"     : LocalConfig,
}
