from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required
from marshmallow import ValidationError

from src import schemas
from src.routes.v1 import router
from src.services.user import UserService


@router.route("/get/<int:user_id>", methods=["GET"])
def get_user_account(user_id):
    user_agent = request.headers.get("user-agent", "unknown")

    user = UserService.get_user_by_id(user_id=user_id, user_agent=user_agent)
    user_roles = ",".join([role.role_name for role in user.roles])
    UserService.add_account_views(user.id, user_agent)

    return {
        # "avatar": user.avatar,
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
        # "avatar": user.avatar,
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
