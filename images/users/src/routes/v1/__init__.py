from flask import Blueprint
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

router = Blueprint("router", __name__)
limiter = Limiter(
  get_remote_address,
  storage_uri="memory://",
  storage_options={"socket_connect_timeout": 30},
  strategy="fixed-window", # or "moving-window"
)

from . import account, auth, learning_center, tutor
