import datetime
import hashlib

from flask import current_app as app

from src.schemas.transaction import PaymentGateway, TransactionStatus, TransactionType
from src.services import TransactionService, UserService


class ClickShopApiService:
    BASE_URL = "https://my.click.uz"

    @classmethod
    def request(cls, data: dict):
        service_id = app.config["CLICK_SERVICE_ID"]
        secret_key = app.config["CLICK_SECRET_KEY"]
        merchant_id = app.config["CLICK_MERCHANT_ID"]
        min_amount = app.config["CLICK_MIN_AMOUNT"]

        if not cls._authorize():
            pass

    @classmethod
    def _prepare(  # noqa: PLR0913
        cls,
        click_trans_id,
        click_paydoc_id,
        merchant_trans_id,
        amount,
        action,
        error,
        error_note,
        sign_time,
        sign_string,
    ):
        user = UserService.get_user_by_phone_number(merchant_trans_id)
        if not user:
            pass

        date_time = datetime.now()
        timestamp = date_time.timestamp()

        transaction = TransactionService.create_transaction(
            user_id=user.id,
            amount=amount,
            transaction_type=TransactionType.INCOME,
            payment_gateway=PaymentGateway.CLICK,
            payment_gateway_id=click_paydoc_id,
            created_at=timestamp,
        )
        result = cls.click_validation(
            merchant_trans_id,
            amount,
            action,
            sign_time,
            sign_string,
            error,
        )
        result["click_trans_id"] = click_trans_id
        result["merchant_trans_id"] = merchant_trans_id
        result["merchant_prepare_id"] = transaction

        return result

    @classmethod
    def _complete(  # noqa: PLR0913
        cls,
        click_trans_id,
        click_paydoc_id,
        merchant_trans_id,
        merchant_prepare_id,
        amount,
        action,
        error,
        error_note,
        sign_time,
        sign_string,
    ):
        transaction = TransactionService.get_transaction_by_id(merchant_prepare_id)

        result = cls.click_validation(
            merchant_trans_id,
            amount,
            action,
            sign_time,
            sign_string,
            error,
            merchant_prepare_id,
        )
        if result["error"] == 0:
            transaction.transaction_status = TransactionStatus.COMPLETED

        result["click_trans_id"] = click_trans_id
        result["merchant_trans_id"] = merchant_trans_id
        result["merchant_confirm_id"] = transaction

        return result

    @classmethod
    def generate_url(cls, user_id: int, amount: int, return_url: str | None = None):
        phone_number = UserService.get_user_by_id(user_id).phone_number[4:]
        service_id = app.config["CLICK_SERVICE_ID"]
        merchant_id = app.config["CLICK_MERCHANT_ID"]

        url = (
            f"{cls.BASE_URL}/services/pay?service_id={service_id}&merchant_id={merchant_id}&amount={amount}&transaction_param={phone_number}"
        )
        if return_url:
            url += f"&return_url={return_url}"
        return url

    @classmethod
    def _authorize(  # noqa: PLR0913
        cls,
        click_trans_id: str,
        sign_string: str,
        merchant_trans_id: str,
        amount: int,
        action: int,
        sign_time: int,
        secret_key: str,
        service_id: str,
        merchant_prepare_id: str | None = None,
    ):
        merchant_prepare_id = merchant_prepare_id if action and action == 1 else ""
        text = (
            f"{click_trans_id}{service_id}{secret_key}{merchant_trans_id}{merchant_prepare_id}{amount}{action}{sign_time}"
        )
        encoded_hash = hashlib.md5(text.encode("utf-8")).hexdigest()    # noqa: S324
        return encoded_hash == sign_string

    @classmethod
    def click_validation(  # noqa: PLR0911 PLR0913
        cls,
        click_trans_id: str,
        merchant_trans_id: str,
        amount: str,
        action: str,
        sign_time: str,
        sign_string: str,
        error: str,
        secret_key: str,
        service_id: str,
        min_amount: int,
        merchant_prepare_id: str | None = None,
    ) -> dict:

        merchant_prepare_id = merchant_prepare_id if action and action == 1 else ""
        text = (
            f"{click_trans_id}{service_id}{secret_key}{merchant_trans_id}{merchant_prepare_id}{amount}{action}{sign_time}"
        )
        encoded_hash = hashlib.md5(text.encode("utf-8")).hexdigest()
        if encoded_hash != sign_string:
            return {
                "error": -1,
                "error_note": "SIGN CHECK FAILED!",
            }

        if action not in [0, 1]:
            return {
                "error": -3,
                "error_note": "Action not found",
            }

        transaction = TransactionService.get_transaction_by_gateway_id(merchant_trans_id)

        if not transaction:
            return {
                "error": -6,
                "error_note": "Transaction does not exist",
            }

        if amount < min_amount:
            return {
                "error": -2	,
                "error_note": "Incorrect parameter amount",
            }

        if transaction.transaction_status == TransactionStatus.COMPLETED:
            return {
                "error": -4,
                "error_note": "Already paid",
            }

        if (transaction.transaction_status == TransactionStatus.CANCELLED
            or int(error) < 0):
            return {
                "error": -9,
                "error_note": "Transaction cancelled",
            }
        return {
            "error": 0,
            "error_note": "Success",
        }
