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

    class Meta:
        verbose_name = _("Service")
        verbose_name_plural = _("Services")
        db_table = "services"

    def __str__(self) -> str:
        return self.name
