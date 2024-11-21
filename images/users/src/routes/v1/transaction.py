from flask import request
from flask_jwt_extended import get_jwt_identity, jwt_required

from src.routes.v1 import router
from src.schemas import PaymentGateway, TransactionStatus
from src.services.transaction import TransactionService


@router.route("/fill", methods=["POST"])
@jwt_required(fresh=True)
def fill_balance():
    user_id=get_jwt_identity()
    amount = request.json

    _id = TransactionService.fill_balance(
        user_id=user_id,
        amount=amount.get("amount"),
        payment_gateway=PaymentGateway.PAYME,
        transaction_status=TransactionStatus.COMPLETED,
    )

    return {"success": str(_id)}, 200


@router.route("/history", methods=["GET"])
@jwt_required(fresh=True)
def get_transactions():
    user_id=get_jwt_identity()

    transactions = TransactionService.get_user_transactions(user_id=user_id)

    return [
        {
            "_id": transaction.id,
            "type": transaction.transaction_type,
            "status": transaction.transaction_status,
            "payment_gateway": transaction.payment_gateway,
            "amount": transaction.amount,
            "service": transaction.content_type.name if transaction.content_type else "wallet",
            "created_at": transaction.created_at,
        }
        for transaction in transactions
    ], 200


@router.route("/buy/premium", methods=["POST"])
@jwt_required(fresh=True)
def buy_premium():
    user_id=get_jwt_identity()
    data = request.json

    amount = data.get("amount")
    service_id = data.get("service_id")

    _id = TransactionService.get_premium(
        user_id=user_id,
        amount=amount,
        service_id=service_id,
    )

    return {"success": str(_id)}, 200
