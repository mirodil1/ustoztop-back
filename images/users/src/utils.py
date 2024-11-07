import secrets

from flask import current_app as app


def generate_security_code():
    return "".join(str(secrets.choice(range(1000, 9999))))


def allowed_file(filename):
    return "." in filename and \
           filename.rsplit(".", 1)[1].lower() in app.config["ALLOWED_EXTENSIONS"]
