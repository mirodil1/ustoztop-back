import json
import random
import string
from urllib.parse import urlencode
from urllib.request import urlopen

from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required

from src import schemas
from src.services.user import UserService

from src.routes.v1 import router


@router.route("/register", methods=["POST"])
def create_account():
    print("CREATE")
    user_data = request.json
    print(user_data)
    schemas.UserSchema().load(user_data)
    phone_number = user_data.get("phone_number")
    password = user_data.get('password')

    UserService.create_user(phone_number=phone_number, password=password)
    return {"error": "no error", "detail": 'Account created successfully'}, 201


@router.route("/send-code", methods=["GET"])
def send_otp():
    pass