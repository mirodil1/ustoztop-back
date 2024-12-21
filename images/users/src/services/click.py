import hashlib

from flask import current_app as app

from src.exceptions import (
    ActionNotFound,
    AlreadyPaid,
    IncorrectParameterAmount,
    SignCheckFailed,
    TransactionCanceled,
    TransactionDoesNotExist,
    UserDoesNotExist,
)
from src.services import TransactionService, UserService


class ClickShopApiService:
    BASE_URL = "https://my.click.uz"

    SERVICE_ID = app.config["CLICK_SERVICE_ID"]
    SECRET_KEY = app.config["CLICK_SECRET_KEY"]
    MERCHANT_ID = app.config["CLICK_MERCHANT_ID"]
    MIN_AMOUNT = app.config["CLICK_MIN_AMOUNT"]

    @classmethod
    def request(cls):
        if not cls._authorize():
            raise SignCheckFailed

    @staticmethod
    def _prepare(  # noqa: PLR0913
        click_trans_id,
        service_id,
        click_paydoc_id,
        merchant_trans_id,
        amount,
        action,
        error,
        error_note,
        sign_time,
        sign_string,
    ):
        pass

    @staticmethod
    def _complete(  # noqa: PLR0913
        click_trans_id,
        service_id,
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
        pass

    @classmethod
    def generate_url(cls, phone_number: str, amount: int, return_url: str | None = None):
        user = UserService.get_user_by_phone_number(phone_number)
        if not user:
            raise UserDoesNotExist
        url = (
            f"{cls.BASE_URL}/services/pay?service_id={cls.SERVICE_ID}&merchant_id={cls.MERCHANT_ID}&amount={amount}&transaction_param={phone_number}"
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
    ):
        text = (
            f"{click_trans_id}{cls.SERVICE_ID}{cls.SECRET_KEY}{merchant_trans_id}{amount}{action}{sign_time}"
        )
        encoded_hash = hashlib.md5(text.encode("utf-8")).hexdigest()    # noqa: S324
        return encoded_hash == sign_string
