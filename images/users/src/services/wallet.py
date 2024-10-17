from src.db import db
from src.models import Wallet


class WalletService:

    @staticmethod
    def create_wallet(user_id):
        wallet = Wallet(user_id=user_id)
        db.session.add(wallet)
        db.session.commit()
