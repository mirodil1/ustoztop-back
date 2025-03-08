from src.db import db
from src.models import Wallet


class WalletService:

    @staticmethod
    def create_wallet(user_id, balance=100000):
        wallet = Wallet(user_id=user_id, balance=balance)
        db.session.add(wallet)
        db.session.commit()
