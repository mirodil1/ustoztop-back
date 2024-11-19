import requests
from flask import current_app as app
from sqlalchemy import desc
from sqlalchemy.orm import joinedload, selectinload
from werkzeug.security import check_password_hash, generate_password_hash

from src.db import db
from src.exceptions import UnknownUser, UsernameAlreadyExists
from src.models import Role, Tutor, User, Location, UserTag
from src.utils import generate_username


class UserService:

    @staticmethod
    def get_user_by_phone_number(phone_number):
        user = User.query.filter_by(phone_number=phone_number).first()
        return user

    @classmethod
    def get_user_by_id(cls, user_id):
        user = User.query.filter_by(id=user_id).first()
        if not user:
            raise UnknownUser
        return user

    @classmethod
    def get_users(cls, gender: str | None, role_name: str | None):
        query = User.query
        if gender:
            query = query.join(User.tutor).filter(Tutor.gender == gender)
        if role_name:
            query = query.join(User.roles).filter(Role.role_name == role_name)
        users = query.all()
        if not users:
            raise UnknownUser
        return users

    @staticmethod
    def get_premium_users():
        premium_users = User.query.filter_by(is_premium=True) \
            .options(
                joinedload(User.learning_center),
                joinedload(User.tutor),
                joinedload(User.location),
                selectinload(User.tags),
            ) \
            .order_by(desc(User.premium_started)).all()
        return premium_users

    @staticmethod
    def create_user(phone_number, password, role_name):
        username = generate_username()
        user = User(phone_number=phone_number, password=password, username=username)
        user.password = generate_password_hash(
            user.password, method="pbkdf2:sha256:5", salt_length=8,
        )
        db.session.add(user)
        db.session.commit()

        from . import RoleService, WalletService
        WalletService.create_wallet(user_id=user.id)
        RoleService.add_user_role(user.id, role_name)

        if role_name == "tutor":
            from . import TutorService
            TutorService.create_tutor(user_id=user.id)
        elif role_name == "learning_center":
            from . import LearningCenterService
            LearningCenterService.create_center(user_id=user.id)

    @classmethod
    def update_user(cls, user_id, **user_new_data):
        user = cls.get_user_by_id(user_id)

        location_data = user_new_data.pop("location", None)
        tags_data = user_new_data.pop("tags", None)

        if location_data:
            location = Location(**location_data)
            db.session.add(location)
            user.location = location

        if tags_data:
            db.session.query(UserTag).filter_by(user_id=user.id).delete()
            for tag in tags_data:
                user_tag = UserTag(user_id=user.id, category_id=tag)
                db.session.add(user_tag)

        for key, value in user_new_data.items():
            if key == "password":
                setattr(
                    user,
                    key,
                    generate_password_hash(user_new_data[key],
                    method="pbkdf2:sha256:5", salt_length=8),
                )
            if key == "username":
                exist = User.query.filter_by(username=user_new_data[key]).filter(
                    User.id != user.id
                ).first()
                if exist:
                    raise UsernameAlreadyExists
                setattr(user, key, value)

            elif key not in ["id", "is_premium"]:
                setattr(user, key, value)
            else:
                raise Exception("insufficient privileges")
        db.session.add(user)
        db.session.commit()

    @classmethod
    def check_user_password(cls, phone_number, plaintext_password):
        user = cls.get_user_by_phone_number(phone_number)
        if user:
            return check_password_hash(user.password, plaintext_password)
        return False

    @staticmethod
    def add_account_views(user_id: int, user_agent:str):
        response = requests.post(
            f"{app.config['STATISTICS_URL']}/api/v1/statistics/account_views/create/{user_id}",
            headers={"user-agent": user_agent},
        )
        if response.status_code == 200:
            return response.status_code
