from enum import Enum


class TransactionStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELED = "canceled"


class TransactionType(str, Enum):
    INCOME = "income"
    OUTCOME = "outcome"


class PaymentGateway(str, Enum):
    PAYME = "payme"
    CLICK = "click"
    PAYNET = "paynet"
    WALLET = "wallet"
