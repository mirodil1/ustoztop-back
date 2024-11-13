import string
import random
import secrets

from flask import current_app as app


def generate_security_code() -> str:
    return "".join(str(secrets.choice(range(1000, 9999))))

def generate_username() -> str:
    prefix = "ustoz_"
    random_part = "".join(random.choices(string.ascii_lowercase + string.digits, k=7)) # noqa: S311
    return f"{prefix}{random_part}"


def allowed_file(filename) -> str:
    return "." in filename and \
           filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]
