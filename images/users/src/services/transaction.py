import datetime
import uuid

from src.db import db
from src.exceptions import InsufficientFunds, InvalidAmount
from src.models import ContentType, Transaction
from src.schemas import PaymentGateway, TransactionStatus, TransactionType
from src.services import UserService


class TransactionService:

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
        user_id: int,
        amount: float,
        payment_gateway: PaymentGateway,
        transaction_status: TransactionStatus,
    ):
        if not isinstance(amount, int) or amount <= 0:
            raise InvalidAmount
        user = UserService.get_user_by_id(user_id)
        user.wallets.balance += amount

        transaction_id = cls.create_transaction(
            user_id=user_id,
            amount=amount,
            transaction_type=TransactionType.INCOME,
            payment_gateway=payment_gateway,
            transaction_status=transaction_status,
        )

        db.session.commit()
        return transaction_id

    @classmethod
    def get_premium(cls, user_id: int, amount: float, service_id: uuid.UUID):
        user = UserService.get_user_by_id(user_id)
        start = datetime.datetime.now()
        expire = start + datetime.timedelta(days=30)

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
        )
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
