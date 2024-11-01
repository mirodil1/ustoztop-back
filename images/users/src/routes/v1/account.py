from flask import current_app as app
from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from marshmallow import ValidationError

from src import schemas
from src.routes.v1 import router
from src.services.user import UserService


@router.route("/get/<int:user_id>", methods=["GET"])
def get_user_account(user_id):
    user_agent = request.headers.get("user-agent", "unknown")

    user = UserService.get_user_by_id(user_id=user_id)
    user_roles = ",".join([role.role_name for role in user.roles])
    UserService.add_account_views(user.id, user_agent)

    return {
        "phone_number": user.phone_number,
        "web_link": user.web_link,
        "facebook_link": user.facebook_link,
        "insta_link": user.insta_link,
        "telegram_link": user.telegram_link,
        "is_verified_by_admin": user.is_verified_by_admin,
        "is_premium": user.is_premium,
        "roles": user_roles,
    }, 200


@router.route("/me", methods=["GET"])
@jwt_required(fresh=True)
def get_me():
    user = UserService.get_user_by_id(user_id=get_jwt_identity())
    user_roles = ",".join([role.role_name for role in user.roles])

    return {
        "phone_number": user.phone_number,
        "web_link": user.web_link,
        "facebook_link": user.facebook_link,
        "insta_link": user.insta_link,
        "telegram_link": user.telegram_link,
        "is_verified_by_admin": user.is_verified_by_admin,
        "is_premium": user.is_premium,
        "roles": user_roles,
        "wallet": {
            "id": user.wallets.id,
            "balance": user.wallets.balance,
        } if user.wallets else None,
    }, 200


@router.route("/update", methods=["PUT"])
@jwt_required(fresh=True)
def update_user_account():
    user_data = request.json
    user_id = get_jwt_identity()

    schemas.UserUpdateSchema().load(user_data)

    user = UserService.get_user_by_id(user_id=user_id)
    UserService.update_user(
        user_id=user_id,
        **user_data,
    )
    return {"error": "no error", "detail": "Account updated successfully"}, 200


@router.route("/premium", methods=["GET"])
def get_premium_accounts():
    premium_users = UserService.get_premium_users()
    users_data = []
    for user in premium_users:
        user_info = {
            "id": user.id,
            "role": ",".join([role.role_name for role in user.roles]),
            "avatar": None,
            "is_verified_by_admin": user.is_verified_by_admin,
            "is_premium": user.is_premium,
        }
        if user.tutor:
            user_info["avatar"] = f"{app.config['BASE_URL']}/media/avatar{user.tutor.avatar}"
            user_info["first_name"] = user.tutor.first_name
            user_info["last_name"] = user.tutor.last_name
        elif user.learning_center:
            user_info["name"] = user.learning_center.name
            user_info["description"] = user.learning_center.description
            user_info["avatar"] = f"{app.config['BASE_URL']}/media/avatar{user.learning_center.avatar}"

        users_data.append(user_info)

    return users_data, 200


@router.route("/get/idx", methods=["GET"])
def get_accounts_ids():
    gender = request.args.get("gender")
    role_name = request.args.get("role")

    users = UserService.get_users(gender, role_name)
    users_data = [{
            "id": user.id,
            # Add any other fields you want to return
        } for user in users]
    return users_data, 200

