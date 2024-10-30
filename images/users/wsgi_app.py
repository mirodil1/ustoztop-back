from gevent import monkey

monkey.patch_all()

import os

from config import config_dict
from gevent.pywsgi import WSGIServer
from src import create_app  # noqa: E402,F401

# WARNING: Don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", "True") == "True"
get_config_mode = "Local" if DEBUG else "Production"

try:

    # Load configuration using the default values
    app_config = config_dict[get_config_mode.capitalize()]

except KeyError:
    exit("Error: Invalid <config_mode>. Expected values [Local, Production] ")


flask_app = create_app(app_config)
celery_app = flask_app.extensions["celery"]


if __name__ == "__main__":
    if DEBUG:
        flask_app.run(host="0.0.0.0", debug=DEBUG)
    else:
        http_server = WSGIServer(("0.0.0.0", 5000), flask_app)
        http_server.serve_forever()
