import uuid

from src import models
from src.cache import redis_db
from src.db import db
from src.exceptions import DeviceAlreadyExists, UnknownDevice


class DeviceService:

    @staticmethod
    def get_device_by_id(device_id):
        device = models.Device.query.filter_by(id=uuid.UUID(device_id)).first()
        if not device:
            raise UnknownDevice
        return device

    @staticmethod
    def create_device_auth_request(
        phone_number:str, user_agent: str | None = None,
    ) -> tuple[str, str]:

        device_id = str(uuid.uuid4())
        device_auth_id = str(uuid.uuid4())

        data = {
                "phone_number": phone_number,
                "device_id": device_id,
                "user_agent": user_agent,
        }

        redis_db.hset(name=device_auth_id, mapping=data)
        redis_db.expire(name=device_auth_id, time=60 * 60 * 3)

        return device_id, device_auth_id

    @staticmethod
    def is_device_registered(phone_number, device_id):
        from . import UserService

        user = UserService.get_user_by_phone_number(phone_number)
        device_exists = db.session.query(models.User, models.Device).filter(
            models.Device.id == device_id,
        ).one_or_none()
        return device_exists

    @staticmethod
    def authorize_device(device_auth_id):
        from . import UserService

        device_data = redis_db.hgetall(str(device_auth_id))
        if not device_data:
            raise UnknownDevice

        phone_number = device_data["phone_number"]
        device_id = device_data["device_id"]
        user_agent = device_data["user_agent"]

        user = UserService.get_user_by_phone_number(phone_number)

        device_is_already_registered = db.session.query(models.User, models.Device).filter(
            models.Device.id == device_id,
        ).one_or_none()
        if device_is_already_registered:
            raise DeviceAlreadyExists

        device = models.Device(id=device_id, user_id=user.id, user_agent=user_agent)
        db.session.add(device)
        db.session.commit()

    @classmethod
    def delete_device(cls, device_id):
        device = cls.get_device_by_id(device_id)
        if device:
            db.session.delete(device)
            db.session.commit()
        else:
            raise UnknownDevice
