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
from src.tasks import send_security_code_task

@router.route("/register", methods=["POST"])
def create_account():
    user_data = request.json
    schemas.UserSchema().load(user_data)
    phone_number = user_data.get("phone_number")
    password = user_data.get('password')

    UserService.create_user(phone_number=phone_number, password=password)
    return {"error": "no error", "detail": 'Account created successfully'}, 201


@router.route("/send-code", methods=["GET"])
def send_otp():
    print("REQUESTED")
    send_security_code_task.delay("+99890")
    return {"error": "no error", "detail": "code sent successfully"}, 200