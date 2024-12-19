from flask import jsonify
from marshmallow.exceptions import ValidationError
from werkzeug.exceptions import BadRequest

from src.exceptions import (
    DeviceAlreadyExists,
    IncorrectAmount,
    InsufficientFunds,
    InvalidAmount,
    InvalidEmail,
    InvalidRefreshToken,
    MethodNotFound,
    PermissionDenied,
    PhoneNumberNotFound,
    RequestFailed,
    RoleAlreadyExists,
    TransactionNotFound,
    TransactionStateDisallowed,
    UnknownDevice,
    UnknownUser,
    UsernameAlreadyExists,
    OrderCompleted,
)

from . import router


@router.errorhandler(BadRequest)
def handle_bad_request(e):
    return jsonify({"error": e.description}), e.code


@router.errorhandler(ValidationError)
def handle_validation_error(e):
    return {"error": e.messages}, 400


@router.errorhandler(InvalidRefreshToken)
def handle_invalid_refresh_token(e):
    return {"error": "invalid refresh token"}, 422


@router.errorhandler(UnknownDevice)
def handle_unknown_device(e):
    return {"error": "unknown device"}, 422


@router.errorhandler(DeviceAlreadyExists)
def handle_device_already_exists(e):
    return {"error": "the device has been already activated"}, 422


@router.errorhandler(RoleAlreadyExists)
def handle_role_already_exists(e):
    return {"error": "role already exists"}, 422


@router.errorhandler(InvalidEmail)
def handle_invalid_email(e):
    return {"error": "invalid email"}, 422


@router.errorhandler(UnknownUser)
def handle_unknown_user(e):
    return {"error": "unknown user"}, 422


@router.errorhandler(UsernameAlreadyExists)
def handle_username_already_exists(e):
    return {"error": "username already exists"}, 422


@router.errorhandler(429)
def handle_rate_limit(e):
    return {"error": "too many requests, try again later"}, 429


@router.errorhandler(InsufficientFunds)
def handle_insufficient_funds(e):
    return {"error": "insufficient funds"}, 400


@router.errorhandler(InvalidAmount)
def handle_invalid_amount(e):
    return {"error": "invalid amount"}, 400

@router.errorhandler(RequestFailed)
def handle_request_failed(e):
    return {"error": "request failed"}, 500

# PAYME error handler

@router.errorhandler(PhoneNumberNotFound)
def handle_payme_phone_number(e):
    return {
        "error" : {
            "code" : -31050,
            "message" : {
                "ru" : "Номер телефона не найден",
                "uz" : "Raqam ro'yhatda yo'q",
                "en" : "Phone number not found",
            },
        },
    }, 200


@router.errorhandler(PermissionDenied)
def handle_payme_permission(e):
    return {
        "error" : {
            "code" : -32504,
            "message" : {
                "ru" : "Недостаточно привилегий для выполнения метода",
                "uz" : "Amaliyotni bajarish uchun yetarli imtiyozlar mavjud emas",
                "en" : "Insufficient privileges to perform the method",
            },
        },
    }, 200


@router.errorhandler(TransactionNotFound)
def handle_payme_transaction_not_found(e):
    return {
        "error" : {
            "code" : -31003,
            "message" : {
                "ru" : "Транзакция не найдена",
                "uz" : "Tranzaksiya topilamdi",
                "en" : "Transaction not found",
            },
        },
    }, 200


@router.errorhandler(IncorrectAmount)
def handle_payme_incorrect_amount(e):
    return {
        "error" : {
            "code" : -31001,
            "message" : {
                "ru" : "Неверная сумма",
                "uz" : "Noto'g'ri qiymat",
                "en" : "Invalid amount",
            },
        },
    }, 200


@router.errorhandler(MethodNotFound)
def handle_payme_method(e):
    return {
        "error" : {
            "code" : -32601,
            "message" : {
                "ru" : "Запрашиваемый метод не найден",
                "uz" : "Amaliyot topilmadi",
                "en" : "Requested method not found",
            },
        },
    }, 200


@router.errorhandler(TransactionStateDisallowed)
def handle_payme_transaction_disaalowed(e):
    return {
        "error" : {
            "code" : -31008,
            "message" : {
                "ru" : "Невозможно выполнить операцию",
                "uz" : "Amaliyotni bajarish mumkin emas",
                "en" : "Unable to perform operation",
            },
        },
    }, 200


@router.errorhandler(OrderCompleted)
def handle_payme_order_completed(e):
    return {
        "error" : {
            "code" : -31007,
            "message" : {
                "ru" : "Заказ выполнен. Невозможно отменить транзакцию. \
                        Товар или услуга предоставлена покупателю в полном объеме",
                "uz" : "Buyurtma bajarildi. Bitimni bekor qilish mumkin emas. \
                        Tovar yoki xizmat xaridorga to'liq hajmda taqdim etilgan",
                "en" : "The order is completed. It is not possible to cancel the transaction.\
                        The product or service is provided to the buyer in full",
            },
        },
    }, 200
