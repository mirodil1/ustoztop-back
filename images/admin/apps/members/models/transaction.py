import uuid
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.members.models import User


class ContentTypes(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=80, null=True, blank=True)
    object_id = models.IntegerField()
    service_id = models.UUIDField()

    class Meta:
        db_table = 'content_types'

    def __str__(self):
        return self.name or str(self.id)


class Transaction(models.Model):
    class TransactionType(models.TextChoices):
        INCOME = "income", "Income"
        OUTCOME = "outcome", "Outcome"

    class PaymentGateway(models.TextChoices):
        PAYME = "payme", "Payme"
        CLICK = "click", "Click"
        PAYNET = "paynet", "Paynet"
        WALLET = "wallet", "Wallet"
    
    class TransactionStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        COMPLETED = "completed", "Completed"
        FAILED = "failed", "Failed"
        CANCELED = "canceled", "Canceled"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(to=User, on_delete=models.DO_NOTHING)
    amount = models.DecimalField(max_digits=14, decimal_places=2)
    transaction_type = models.CharField(
        max_length=10,
        choices=TransactionType.choices
    )
    payment_gateway = models.CharField(
        max_length=10, choices=PaymentGateway.choices, null=True, blank=True
    )
    payment_gateway_id = models.CharField(max_length=255, null=True, blank=True)
    payment_gateway_time = models.BigIntegerField(null=True, blank=True)
    transaction_status = models.CharField(
        max_length=10, choices=TransactionStatus.choices, default=TransactionStatus.PENDING
    )
    content_type = models.ForeignKey(to=ContentTypes, on_delete=models.DO_NOTHING, null=True, blank=True)
    state = models.IntegerField(null=True, blank=True)
    reason = models.IntegerField(null=True, blank=True)
    canceled_at = models.BigIntegerField(default=0, null=True, blank=True)
    performed_at = models.BigIntegerField(null=True, blank=True)
    created_at = models.BigIntegerField()

    class Meta:
        db_table = "transactions"

    def __str__(self):
        return f"Transaction {self.id}, Amount: {self.amount}"
