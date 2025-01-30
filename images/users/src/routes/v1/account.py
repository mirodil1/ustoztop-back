from flask import current_app as app
from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required

from src import schemas
from src.routes.v1 import router
from src.services.user import UserService


@router.route("/get/<int:user_id>", methods=["GET"])
def get_user_account(user_id):
    user_agent = request.headers.get("user-agent", "unknown")

    user = UserService.get_user_by_id(user_id=user_id)
    user_roles = ",".join([role.role_name for role in user.roles])

    response = {
        "roles": user_roles,
        "is_verified_by_admin": user.is_verified_by_admin,
        "is_premium": user.is_premium,
        "joined_date": user.created_at,
    }
    if user.tutor:
        response["avatar"] = (
            f"{app.config['BASE_URL']}/media/uploads/avatar/{user.tutor.avatar}"
            if user.tutor.avatar else None
        )
        response["first_name"] = user.tutor.first_name
        response["last_name"] = user.tutor.last_name

        if user.is_premium:
            response.update(
                {
                    "description": user.tutor.description,
                    "gender": user.tutor.gender.name if user.tutor.gender else None,
                    "education": [
                        {
                            "id": education.id,
                            "name": education.name,
                            "degree": education.degree.name,
                            "field_of_study": education.field_of_study,
                            "start_year": education.start_year,
                            "finish_year": education.finish_year,
                        }
                        for education in user.tutor.education
                    ],
                    "language": [
                        {
                            "id": language.id,
                            "name": language.name,
                            "level": language.level.name,
                        }
                        for language in user.tutor.language
                    ],
                    "experience": [
                        {
                            "id": experience.id,
                            "organization": experience.organization,
                            "position": experience.position,
                            "start_year": experience.start_year,
                            "finish_year": experience.finish_year,
                            "is_working": experience.is_working,
                        }
                        for experience in user.tutor.experience
                    ],
                }
            )
            UserService.add_account_views(user.id, user_agent)
    elif user.learning_center:
        response["name"] = user.learning_center.name
        response["avatar"] = (
            f"{app.config['BASE_URL']}/media/uploads/avatar/{user.learning_center.avatar}"
            if user.learning_center.avatar else None
        )
        if user.is_premium:
            response.update(
                {
                    "description": user.learning_center.description,
                    "banner": (
                        f"{app.config['BASE_URL']}/media/uploads/banner/{user.learning_center.avatar}"
                        if user.learning_center.avatar else None
                    ),
                    "branches": [
                        {
                            "id": branch.id,
                            "name": branch.name,
                        } for branch in user.learning_center.branch
                    ],
                    "schedule": [
                        {
                            "id": schedule.id,
                            "day_of_week": schedule.day_of_week.name,
                            "opening_time": schedule.opening_time.strftime("%H:%M"),
                            "closing_time": schedule.closing_time.strftime("%H:%M"),
                            "is_closed": schedule.is_closed,
                        } for schedule in user.learning_center.working_schedule
                    ],
                }
            )
            UserService.add_account_views(user.id, user_agent)
    return response, 200


@router.route("/me", methods=["GET"])
@jwt_required(fresh=True)
def get_me():
    user = UserService.get_user_by_id(user_id=get_jwt_identity())
    user_roles = ",".join([role.role_name for role in user.roles])
    user_data = {
        "id": user.id,
        "phone_number": user.phone_number,
        "username": user.username,
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
        "location": {
                "uz": user.location.uz,
                "ru": user.location.ru,
                "latitude": user.location.latitude,
                "longitude": user.location.latitude,
            } if user.location else None,
        "tags": [
            tag.category_id for tag in user.tags
        ],
        "joined_date": user.created_at,
    }
    if user.tutor:
        user_data["avatar"] = (
            f"{app.config['BASE_URL']}/media/uploads/avatar/{user.tutor.avatar}"
            if user.tutor.avatar else None
        )
        user_data["first_name"] = user.tutor.first_name
        user_data["last_name"] = user.tutor.last_name
        user_data["description"] = user.tutor.description
        user_data["gender"] = user.tutor.gender.name if user.tutor.gender else None
        user_data["education"] = [
            {
                "id": education.id,
                "name": education.name,
                "degree": education.degree.name,
                "start_year": education.start_year,
                "finish_year": education.finish_year,
            }
            for education in user.tutor.education
        ]
        user_data["language"] = [
            {
                "id": language.id,
                "name": language.name,
                "level": language.level.name,
            }
            for language in user.tutor.language
        ]
        user_data["experience"] = [
            {
                "id": experience.id,
                "organization": experience.organization,
                "position": experience.position,
                "start_year": experience.start_year,
                "finish_year": experience.finish_year,
                "is_working": experience.is_working,
            }
            for experience in user.tutor.experience
        ]
    elif user.learning_center:
        user_data["name"] = user.learning_center.name
        user_data["description"] = user.learning_center.description
        user_data["avatar"] = (
            f"{app.config['BASE_URL']}/media/uploads/avatar/{user.learning_center.avatar}"
            if user.learning_center.avatar else None
        )
        user_data["branches"] = [
            {
                "id": branch.id,
                "name": branch.name,
            } for branch in user.learning_center.branch
        ]
        user_data["schedule"] = [
            {
                "id": schedule.id,
                "day_of_week": schedule.day_of_week.name,
                "opening_time": schedule.opening_time.strftime("%H:%M"),
                "closing_time": schedule.closing_time.strftime("%H:%M"),
                "is_closed": schedule.is_closed,
            } for schedule in user.learning_center.working_schedule
        ]
    return user_data, 200


@router.route("/update", methods=["PUT"])
@jwt_required(fresh=True)
def update_user_account():
    user_data = request.json
    user_id = get_jwt_identity()

    schemas.UserUpdateSchema().load(user_data)

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
            "roles": ",".join([role.role_name for role in user.roles]),
            "username": user.username,
            "avatar": None,
            "is_verified_by_admin": user.is_verified_by_admin,
            "location": {
                "uz": user.location.uz,
                "ru": user.location.ru,
                "latitude": user.location.latitude,
                "longitude": user.location.latitude,
            } if user.location else None,
            "is_premium": user.is_premium,
            "tags": [
                tag.category_id for tag in user.tags
            ],
        }
        if user.tutor:
            user_info["avatar"] = (
                f"{app.config['BASE_URL']}/media/uploads/avatar/{user.tutor.avatar}"
                if user.tutor.avatar else None
            )
            user_info["first_name"] = user.tutor.first_name
            user_info["last_name"] = user.tutor.last_name
            user_info["description"] = user.tutor.description
        elif user.learning_center:
            user_info["name"] = user.learning_center.name
            user_info["description"] = user.learning_center.description
            user_info["avatar"] = (
                f"{app.config['BASE_URL']}/media/uploads/avatar/{user.learning_center.avatar}"
                if user.learning_center.avatar else None
            )

        users_data.append(user_info)

    return users_data, 200


@router.route("/get/idx", methods=["GET"])
def get_accounts_ids():
    gender = request.args.get("gender")
    role_name = request.args.get("role")

    users = UserService.get_users(gender, role_name)
    users_data = [{
            "id": user.id,
        } for user in users]
    return users_data, 200


@router.route("/get/info/<int:user_id>", methods=["GET"])
def get_accounts_info(user_id):
    user = UserService.get_user_by_id(user_id)
    user_roles = ",".join([role.role_name for role in user.roles])
    user_info = {
        "roles": user_roles,
    }

    if user.tutor:
        user_info["first_name"] = user.tutor.first_name
        user_info["last_name"] = user.tutor.last_name
    elif user.learning_center:
        user_info["name"] = user.learning_center.name

    return user_info, 200
