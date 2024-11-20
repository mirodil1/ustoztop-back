import uuid

from flask import current_app as app
from sqlalchemy import desc
from sqlalchemy.orm import joinedload, selectinload


from src.db import db
from src.exceptions import UnknownUser, UsernameAlreadyExists
from src.models import Transaction


class TransactionService:

    @staticmethod
    def create_transaction(**transaction_data):
        pass

    @staticmethod
    def get_user_transactions(user_id: int):
        pass

    @staticmethod
    def fill_balance(user_id: int, amount: float):
        pass

    @staticmethod
    def withdraw_from_wallet(user_id: int, amount: float):
        pass
