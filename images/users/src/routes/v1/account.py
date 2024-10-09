import json
import random
import string
from urllib.parse import urlencode
from urllib.request import urlopen

from celery import shared_task
from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required

from src import schemas
from src.routes.v1 import router
from src.services.device import DeviceService
from src.services.history import HistoryService
from src.services.sms import SMSService
from src.services.token import TokenService
from src.services.user import UserService
from src.tasks import send_security_code_task


@router.route("/get/<int:user_id>", methods=["GET"])
def get_user_account(user_id):
    user = UserService.get_user_by_id(user_id=user_id)
    user_roles = [{"id": role.id, "name": role.role_name} for role in user.roles]

    return {
        "avatar": user.avatar,
        "phone_number": user.phone_number,
        "web_link": user.web_link,
        "facebook_link": user.facebook_link,
        "insta_link": user.insta_link,
        "telegram_link": user.telegram_link,
        "is_verified_by_admin": user.is_verified_by_admin,
        "is_premium": user.is_premium,
        "roles": user_roles,
    }, 200
