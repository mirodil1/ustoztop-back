import requests

from werkzeug.security import check_password_hash, generate_password_hash
from flask import current_app as app

from src.db import db
from src.exceptions import UnknownUser
from src.models import User

class UserService:

    @staticmethod
    def get_user_by_phone_number(phone_number):
        user = User.query.filter_by(phone_number=phone_number).first()
        return user

    @classmethod
    def get_user_by_id(cls, user_id, user_agent: str):
        user = User.query.filter_by(id=user_id).first()
        if not user:
            raise UnknownUser
        cls._add_account_views(user.id, user_agent)
        return user

    @staticmethod
    def create_user(phone_number, password, role_name):
        user = User(phone_number=phone_number, password=password)
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

        for key, value in user_new_data.items():
            if key == "password":
                setattr(
                    user,
                    key,
                    generate_password_hash(user_new_data[key],
                    method="pbkdf2:sha256:5", salt_length=8),
                )
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
    def _add_account_views(user_id: int, user_agent:str):
        response = requests.post(
            f"{app.config['STATISTICS_URL']}/v1/statistics/account_views/create/{user_id}",
            headers={"user-agent": user_agent}
        )
        if response.status_code == 200:
            print(response.json())
        print(response)
