from werkzeug.security import check_password_hash, generate_password_hash

from src.db import db
from src.exceptions import UnknownUser
from src.models import User


class UserService:

    @staticmethod
    def get_user_by_phone_number(phone_number):
        user = User.query.filter_by(phone_number=phone_number).first()
        return user

    @staticmethod
    def get_user_by_id(user_id):
        user = User.query.filter_by(id=user_id).first()
        if not user:
            raise UnknownUser
        return user

    @staticmethod
    def create_user(phone_number, password):
        user = User(phone_number=phone_number, password=password)
        user.password = generate_password_hash(
            user.password, method="pbkdf2:sha256:5", salt_length=8,
        )
        db.session.add(user)
        db.session.commit()

    @classmethod
    def update_user(cls, user_id, **user_new_data):
        user = cls.get_user_by_id(user_id)

        for key, value in user_new_data.items():
            if key == "password":
                setattr(
                    user,
                    key,
                    generate_password_hash(user_new_data[key],
                    method="pbkdf2:sha256:5", salt_length=8)
                )
            elif key not in ["id", "is_premium"]:
                setattr(user, key, user_new_data[key])
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
