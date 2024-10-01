from flask import Blueprint

router = Blueprint("router", __name__)

from . import auth
