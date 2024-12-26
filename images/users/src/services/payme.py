import base64
import binascii
from datetime import datetime

from flask import current_app as app

from src.db import db
from src.exceptions import (
    IncorrectAmount,
    MethodNotFound,
    PermissionDenied,
    PhoneNumberNotFound,
    TransactionNotFound,
    TransactionStateDisallowed,
)
from src.schemas import PaymentGateway, TransactionStatus, TransactionType
from src.services import TransactionService, UserService


class PaymeService:
    CHECK_PERFORM_TRANSACTION = "CheckPerformTransaction"
    CREATE_TRANSACTION = "CreateTransaction"
    PERFORM_TRANSACTION = "PerformTransaction"
    CANCEL_TRANSACTION = "CancelTransaction"
    CHECK_TRANSACTION = "CheckTransaction"
    GET_STATEMENT = "GetStatement"

    # MIN_AMOUNT = app.config["PAYME_MIN_AMOUNT"]
    # TRANSACTION_TIMEOUT = app.config["PAYME_TRANSACTION_TIMEOUT"]
    # MERCHANT_ID = app.config["PAYME_MERCHANT_ID"]
    PAYME_CHECKOUT_URL = "https://checkout.paycom.uz"

    @classmethod
    def _request(cls, password: str, data: dict):
        is_authorized = cls._authorize(password)
        if is_authorized:
            method = data.get("method")
            params = data.get("params")

            if method == cls.CHECK_PERFORM_TRANSACTION:
                result = cls._check_perform_transaction(params)
            elif method == cls.CREATE_TRANSACTION:
                result = cls._create_transaction(params)
            elif method == cls.PERFORM_TRANSACTION:
                result = cls._perform_transaction(params)
            elif method == cls.CANCEL_TRANSACTION:
                result = cls._cancel_transaction(params)
            elif method == cls.CHECK_TRANSACTION:
                result = cls._check_transaction(params)
            elif method == cls.GET_STATEMENT:
                result = cls._get_statement(params)
            else:
                raise MethodNotFound
        else:
            raise PermissionDenied
        return result

    @classmethod
    def _check_perform_transaction(cls, params: dict):
        amount = params.get("amount")
        phone_number = params.get("phone_number")

        if amount < app.config["PAYME_MIN_AMOUNT"]:
            raise IncorrectAmount

        user = UserService.get_user_by_phone_number(phone_number)

        if not user:
            raise PhoneNumberNotFound

        return {
            "result" : {
                "allow" : True,
            },
        }

    @classmethod
    def _create_transaction(cls, params: dict):
        amount = params.get("amount")
        transaction_id = params.get("id")
        time = params.get("time")
        phone_number = params.get("account").get("phone_number")
        transaction_timeout = app.config["PAYME_TRANSACTION_TIMEOUT"]

        if amount < app.config["PAYME_MIN_AMOUNT"]:
            raise IncorrectAmount
        user = UserService.get_user_by_phone_number(phone_number)
        if not user:
            raise PhoneNumberNotFound

        transaction = TransactionService.get_transaction_by_gateway_id(transaction_id)
        date_time = datetime.now()
        timestamp = date_time.timestamp()

        if transaction:
            if transaction.state != 1:
                raise TransactionStateDisallowed

            if timestamp - transaction.created_at > transaction_timeout:
                transaction.state = -1
                transaction.reason = 4
                raise TransactionStateDisallowed
        else:
            transaction = TransactionService.create_transaction(
                user=user.id,
                amount=amount,
                transaction_type=TransactionType.INCOME,
                payment_gateway_id=transaction_id,
                payment_gateway=PaymentGateway.PAYME,
                payment_gateway_time=time,
                transaction_status=TransactionStatus.PENDING,
                state=1,
                created_at=timestamp,
            )

        return {
            "result" : {
                "create_time" : transaction.created_at,
                "transaction" : transaction.id,
                "state" : transaction.state,
            },
        }

    @classmethod
    def _check_transaction(cls, params: dict):
        transaction_id = params.get("id")

        transaction = TransactionService.get_transaction_by_gateway_id(transaction_id)
        if not transaction:
            raise TransactionNotFound
        return {
            "result" : {
                "create_time" : transaction.created_at,
                "perform_time" : transaction.performed_at,
                "cancel_time" : transaction.canceled_at,
                "transaction" : transaction.id,
                "state" : transaction.state,
                "reason" : transaction.reason,
            },
        }

    @classmethod
    def _perform_transaction(cls, params: dict):
        transaction_id = params.get("id")
        transaction_timeout = app.config["PAYME_TRANSACTION_TIMEOUT"]

        transaction = TransactionService.get_transaction_by_gateway_id(transaction_id)
        if not transaction:
            raise TransactionNotFound
        if transaction.state != 1:
            if transaction.state == 2:
                return {
                    "result" : {
                        "transaction" : transaction.id,
                        "perform_time" : transaction.perform_time,
                        "state" : transaction.state,
                    },
                }
            raise TransactionStateDisallowed

        date_time = datetime.now()
        timestamp = date_time.timestamp()

        if timestamp - transaction.created_at > transaction_timeout:
            transaction.state = -1
            transaction.reason = 4
            raise TransactionStateDisallowed
        TransactionService.fill_balance(
            transaction_id=transaction.id,
            user_id=transaction.user_id,
            amount=transaction.amount,
            perform_time=timestamp,
        )
        return {
            "result" : {
                "transaction" : transaction.id,
                "perform_time" : transaction.perform_time,
                "state" : transaction.state,
            },
        }

    @staticmethod
    def _cancel_transaction(params: dict):
        transaction_id = params.get("id")
        reason = params.get("reason")

        transaction = TransactionService.get_transaction_by_gateway_id(transaction_id)
        if not transaction:
            raise TransactionNotFound

        date_time = datetime.now()
        timestamp = date_time.timestamp()

        if transaction.state == 1:
            transaction.state = -1
            transaction.reason = reason
            transaction.canceled_at = timestamp
            db.session.commit()

        elif transaction.state == 2:
            withdraw = TransactionService.withdraw_from_balance(
                transaction.user_id,
                transaction.amount,
            )
            if withdraw:
                transaction.state = -2
                transaction.reason = reason
                transaction.canceled_at = timestamp
                db.session.commit()

        return {
            "result": {
                "state": transaction.state,
                "cancel_time": transaction.canceled_at,
                "transaction": transaction.id,
            },
        }

    @classmethod
    def _get_statement(cls, params: dict):
        from_date = params.get("from")
        to_date = params.get("to")

        transactions = TransactionService.get_transactions(from_date, to_date)
        return {
            "result" : {
                "transactions" : [
                    {
                        "id" : transaction.payment_gateway_id,
                        "time" : transaction.payment_gateway_time,
                        "amount" : transaction.amount,
                        "account" : {
                            "phone_number" : transaction.user.phone_number,
                        },
                        "create_time" : transaction.created_at,
                        "perform_time" : transaction.performed_at,
                        "cancel_time" : transaction.canceled_at,
                        "transaction" : transaction.id,
                        "state" : transaction.state,
                        "reason" : transaction.reason,
                        "reseivers": [],
                    }
                    for transaction in transactions
                ] if transactions else [],
            },
        }

    @classmethod
    def _authorize(cls, password):
        is_authorized = False

        if not isinstance(password, str):
            raise PermissionDenied
        password = password.split()[-1]
        try:
            password = base64.b64decode(password).decode("utf-8")
        except (binascii.Error, UnicodeDecodeError):
            raise PermissionDenied from None

        merchant_key = password.split(":")[-1]
        if merchant_key == app.config["PAYME_SECRET_KEY"]:
            is_authorized = True

        if merchant_key != app.config["PAYME_SECRET_KEY"]:
            raise PermissionDenied

        return is_authorized

    @classmethod
    def generate_url(cls, user_id: int, amount: int):
        merchant_id = app.config["PAYME_MERCHANT_ID"]
        amount = amount * 100
        phone_number = UserService.get_user_by_id(user_id).phone_number

        text = (
            f"m={merchant_id};ac.phone_number={phone_number};a={amount}"
        )
        encoded_path = base64.b64encode(text.encode("utf-8")).decode("utf-8")
        return f"{cls.PAYME_CHECKOUT_URL}/{encoded_path}"
