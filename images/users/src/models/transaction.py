import uuid

from sqlalchemy.dialects.postgresql import ENUM, UUID

from src.db import db
from src.models.core import TimeStampedModel
from src.schemas.transaction import PaymentGateway, TransactionStatus, TransactionType


class ContentType(db.Model):
    __tablename__ = "content_types"

    id = db.Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    name = db.Column(db.String(80), nullable=True)
    object_id = db.Column(db.Integer, nullable=False)
    service_id = db.Column(UUID(as_uuid=True), nullable=False)


class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id", ondelete="NO ACTION"),
        nullable=False,
    )
    amount = db.Column(db.Numeric(14, 2), nullable=False)
    transaction_type = db.Column(
        ENUM(TransactionType, name="transaction_type_enum"),
        nullable=False,
    )
    payment_gateway = db.Column(
        ENUM(PaymentGateway, name="payment_gateway_enum"),
        nullable=True,
    )
    payment_gateway_id = db.Column(db.String, nullable=True)
    payment_gateway_time = db.Column(db.BigInteger, nullable=True)
    transaction_status = db.Column(
        db.Enum(TransactionStatus,name="transaction_status_enum"),
        default=TransactionStatus.PENDING,
        nullable=False,
    )
    content_type_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey("content_types.id", ondelete="NO ACTION"),
        nullable=True,
    )
    state = db.Column(db.Integer, nullable=True)
    reason = db.Column(db.Integer, nullable=True)
    canceled_at = db.Column(db.BigInteger(default=0), nullable=True)
    performed_at = db.Column(db.BigInteger, nullable=True)
    created_at = db.Column(db.BigInteger, nullable=False)

    # Foreign key relationships
    user = db.relationship("User", backref=db.backref("transactions"))
    content_type = db.relationship("ContentType", backref="transactions")

    def __repr__(self):
        return f"<Transaction {self.id}, Amount: {self.amount}>"
