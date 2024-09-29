import os
import logging
from sys import exit

# import api.v1
# import defaults
# import token_store
from authlib.integrations.flask_client import OAuth
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint
from db import postgres
# from storage.db_models import User


logger = logging.getLogger(__name__)
    

def create_app(app_config):
    app = Flask(__name__)
    app.config.from_object(app_config)
    # app.config.from_object(defaults)
    # logging.basicConfig(
    #     level=app.config["LOG_LEVEL"],
    # )

    with app.app_context():
        postgres.init_db()

    return app

