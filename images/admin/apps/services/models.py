import uuid

from django.core.validators import FileExtensionValidator
from django.db import models
from django.template import defaultfilters
from django.utils.translation import gettext_lazy as _
from parler.models import TranslatableModel, TranslatedFields

from apps.core.models import TimeStampedModel


class Service(TimeStampedModel, TranslatableModel):
    """
    Service model
    """
    class ServiceType(models.TextChoices):
        TOP = "top", _("Top")
        PREMIUM = "premium", _("Premium")

    class ServiceAudience(models.TextChoices):
        ALL = "all", _("all")
        TUTOR = "tutor", _("Tutor")
        LEARNING_CENTER = "learning_center", _("Learning Center")

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True)
    translations = TranslatedFields(
        name=models.CharField(max_length=255, verbose_name=_("Name")),
        description=models.CharField(
            max_length=255,
            verbose_name=_("Description"),
        ),
    )
    image = models.FileField(
        upload_to="services",
        validators=[FileExtensionValidator(["svg", "png", "jpg"])],
        verbose_name=_("Image"),
    )
    price = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        verbose_name=_("Price"),
    )
    discount_price = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        verbose_name=_("Discount Price"),
        null=True,
        blank=True,
    )
    service_type = models.CharField(
        max_length=12,
        choices=ServiceType.choices,
        default=ServiceType.TOP,
        verbose_name=_("Service type"),
    )
    service_audience = models.CharField(
        max_length=20,
        choices=ServiceAudience.choices,
        default=ServiceAudience.ALL,
        verbose_name=_("Service audience"),
    )
    duration = models.IntegerField(default=0, verbose_name=_("Duration"))
    is_discount = models.BooleanField(default=False, verbose_name=_("Discount status"))
    is_active = models.BooleanField(default=True, verbose_name=_("Satatus"))

    class Meta:
        verbose_name = _("Service")
        verbose_name_plural = _("Services")
        db_table = "services"

    def __str__(self) -> str:
        return self.name
