from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required

from src import schemas
from src.routes.v1 import limiter, router
from src.services.device import DeviceService
from src.services.history import HistoryService
from src.services.sms import SMSService
from src.services.token import TokenService
from src.services.user import UserService
from src.tasks import send_security_code_task


@router.route("/login", methods=["POST"])
def login():
    user_data = request.json

    user_agent = request.headers.get("User-Agent")

    schemas.UserAuthInfoSchema().load(user_data)
    is_password_correct = UserService.check_user_password(
        user_data["phone_number"], user_data["password"],
    )
    phone_number = user_data["phone_number"]

    if not is_password_correct:
        return {"error": "Wrong phone number or password"}, 401

    device_id = user_data.get("device_id", None)
    if device_id:
        if DeviceService.is_device_registered(
            phone_number=phone_number,
            device_id=device_id,
        ):
            access_token, refresh_token = TokenService.create_token_pair(
                phone_number, device_id,
            )
            HistoryService.add_history_record(device_id)
            return {"access_token": access_token, "refresh_token": refresh_token}, 200
        return {"error": "Unknown device"}, 400

    device_id, device_auth_id = DeviceService.create_device_auth_request(
        phone_number,
        user_agent,
    )
    return {"device_id": device_id, "device_auth_id": device_auth_id}, 200


@router.route("/register", methods=["POST"])
def create_account():
    user_data = request.json
    schemas.UserSchema().load(user_data)
    phone_number = user_data.get("phone_number")
    password = user_data.get("password")
    role = user_data.get("role")
    code = user_data.get("code")

    if UserService.get_user_by_phone_number(phone_number):
        return {
            "error": "Bad request", "detail": "User already registered",
        }, 400
    verified = SMSService.verify_code(phone_number, str(code))
    if verified:
        UserService.create_user(
            phone_number=phone_number,
            password=password,
            role_name=role,
        )
        return {"error": "no error", "detail": "Account created successfully"}, 201
    return {
        "error": "Bad request", "detail": "Something went wrong, please try again",
    }, 400


@router.route("/authorize_device/<uuid:device_auth_id>", methods=["GET"])
def authorize_device(device_auth_id):
    DeviceService.authorize_device(device_auth_id)
    return {"msg": "device activated"}, 200


@router.route("/send-code", methods=["GET"])
@limiter.limit("2/minute")
def send_security_code():
    user_data = request.json
    phone_number = user_data.get("phone_number")
    send_security_code_task.delay(phone_number)
    return {"error": "no error", "detail": "code sent successfully"}, 200


@router.route("/logout", methods=["POST"])
@jwt_required(fresh=True)
def logout():
    user_data = request.json
    schemas.DeviceIdSchema().load(user_data)
    user_id = get_jwt_identity()
    TokenService.remove_refresh_token(user_id, user_data["device_id"])
    return {"error": "no error"}, 200


@router.route("/logout_all", methods=["POST"])
@jwt_required(fresh=True)
def logout_all():
    user_id = get_jwt_identity()
    TokenService.remove_all_refresh_tokens(user_id)
    return {"error": "no error"}, 200
