import base64
import datetime
import uuid

import requests
from flask import current_app as app

from src.db import db
from src.exceptions import (
    InsufficientFunds,
    InvalidAmount,
    OrderCompleted,
    RequestFailed,
)
from src.models import ContentType, Transaction
from src.schemas import PaymentGateway, TransactionStatus, TransactionType
from src.services import UserService
from src.utils import timestamp


class TransactionService:

    @staticmethod
    def get_transaction_by_id(transaction_id: str):
        transaction = Transaction.query.filter_by(id=transaction_id)
        if not transaction:
            return None
        return transaction

    @staticmethod
    def get_transaction_by_gateway_id(transaction_id: str):
        transaction = Transaction.query.filter_by(payment_gateway_id=transaction_id)
        if not transaction:
            return None
        return transaction

    @staticmethod
    def get_transactions(from_date, to_date):
        transactions = Transaction.query.filter(
            Transaction.created_at.between(from_date, to_date),
        )
        return transactions

    @staticmethod
    def create_transaction(**transaction_data):
        transaction = Transaction(**transaction_data)
        db.session.add(transaction)
        db.session.commit()
        return transaction.id

    @staticmethod
    def get_user_transactions(user_id: int):
        transactions = (
            Transaction.query.filter_by(user_id=user_id)
            .order_by(Transaction.created_at.desc())
            .all()
        )
        return transactions

    @classmethod
    def fill_balance(
        cls,
        transaction_id: uuid.UUID,
        user_id: int,
        amount: float,
        perform_time: int,
    ):
        user = UserService.get_user_by_id(user_id)
        transaction = cls.get_transaction_by_id(transaction_id)

        user.wallets.balance += amount

        transaction.state = 2
        transaction.status = TransactionStatus.COMPLETED
        transaction.perform_time = perform_time
        db.session.commit()
        return transaction_id

    @classmethod
    def withdraw_from_balance(
        cls,
        user_id: int,
        amount: int,
    ):
        user = UserService.get_user_by_id(user_id)

        if user.wallets.balance >= amount:
            user.wallets.balance -= amount
            db.session.commit()
            return True
        raise OrderCompleted

    @classmethod
    def get_premium(cls, user_id: int, service_id: uuid.UUID):
        service = cls._get_service(service_id)
        amount = service.get("price")
        duration = service.get("duration")

        user = UserService.get_user_by_id(user_id)
        start = datetime.datetime.now()
        expire = start + datetime.timedelta(days=duration)

        if amount <= 0:
            raise InvalidAmount

        if user.wallets.balance < amount:
            raise InsufficientFunds

        user.wallets.balance-= amount
        if not user.is_premium:
            user.is_premium = True
            user.premium_started = start
            user.premium_expired = expire
        else:
            user.premium_expired = expire

        content_type = cls._create_content_type(
            name="premium",
            obj_id=user_id,
            service_id=service_id,
        )

        transaction_id = cls.create_transaction(
            user_id=user_id,
            amount=amount,
            transaction_type=TransactionType.OUTCOME,
            transaction_status=TransactionStatus.COMPLETED,
            content_type=content_type,
            created_at=timestamp(),
        )
        return transaction_id

    @classmethod
    def promote_announcement(
        cls,
        user_id: int,
        service_id: uuid.UUID,
        announcement_id: int,
    ):
        user = UserService.get_user_by_id(user_id)

        service = cls._get_service(service_id)

        amount = service.get("price")
        duration = service.get("duration")

        if amount <= 0:
            raise InvalidAmount

        if user.wallets.balance < amount:
            raise InsufficientFunds
        user.wallets.balance-= amount

        content_type = cls._create_content_type(
            name="top",
            obj_id=announcement_id,
            service_id=service_id,
        )

        transaction_id = cls.create_transaction(
            user_id=user_id,
            amount=amount,
            transaction_type=TransactionType.OUTCOME,
            transaction_status=TransactionStatus.COMPLETED,
            content_type=content_type,
            created_at=timestamp(),
        )
        data = f"user_id={user_id};ann_id={announcement_id};duration={duration}"
        encoded_data = base64.urlsafe_b64encode(data.encode("utf-8"))
        cls._top_announcement_request(encoded_data)
        return transaction_id

    @staticmethod
    def _create_content_type(name: str, obj_id: int, service_id: uuid.UUID):
        content_type = ContentType(
            name=name,
            object_id=obj_id,
            service_id=service_id,
        )
        db.session.add(content_type)

        return content_type

    @staticmethod
    def _get_service(service_id: uuid.UUID):
        response = requests.get(
            f"{app.config['ANNOUNCEMENTS_URL']}/api/v1/plans/{service_id}",
        )
        if response.status_code == 200:
            return response.json()
        raise RequestFailed

    @staticmethod
    def _get_announcement(announcements_id: int):
        response = requests.get(
            f"{app.config['ANNOUNCEMENTS_URL']}/api/v1/announcements/{announcements_id}",
        )
        if response.status_code == 200:
            return response.json()
        raise RequestFailed

    @staticmethod
    def _top_announcement_request(data):
        response = requests.post(
            url=f"{app.config['ANNOUNCEMENTS_URL']}/api/v1/announcements/promote",
            params={"data": data},
        )
        if response.status_code == 200:
            return response.json()
        raise RequestFailed
