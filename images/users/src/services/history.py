import datetime

from src import models
from src.db import db
from src.exceptions import UnknownDevice

from . import DeviceService


class HistoryService:

    @staticmethod
    def add_history_record(device_id):
        device = DeviceService.get_device_by_id(device_id)
        if not device:
            raise UnknownDevice
        user_id = device.user_id
        login_date = datetime.datetime.now()
        history_record = models.LoginHistoryRecord(
            user_id=user_id,
            device_id=device_id,
            login_date=login_date,
        )
        db.session.add(history_record)
        db.session.commit()

    @staticmethod
    def get_history(email, start_date, end_date):
        from . import UserService

        user_id = UserService.get_user_by_email(email).id
        records = db.session.query(models.LoginHistoryRecord).filter(
            models.LoginHistoryRecord.user_id == user_id).filter(
            models.LoginHistoryRecord.login_date >= start_date).filter(
                models.LoginHistoryRecord.login_date <= end_date,
            )
        result = [
            {
                "device_id": str(record.device_id),
                "login_date": str(record.login_date),
            } for record in records
        ]

        return result
