from gevent import monkey

monkey.patch_all()

import os

from app import create_app  # noqa: E402,F401
from config import config_dict

# WARNING: Don't run with debug turned on in production!
DEBUG = (os.getenv("DEBUG", 'False') == "True")

get_config_mode = "Local" if DEBUG else "Production"

try:

    # Load configuration using the default values
    app_config = config_dict[get_config_mode.capitalize()]

except KeyError:
    exit("Error: Invalid <config_mode>. Expected values [Local, Production] ")


app = create_app(app_config)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=DEBUG)