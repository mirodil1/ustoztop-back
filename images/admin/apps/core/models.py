from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField


class TimeStampedModel(models.Model):
    """
    Abstract Timestamp model
    """

    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated"))

    class Meta:
        abstract = True


class Region(models.Model):

    id = models.AutoField(primary_key=True)
    uz = models.CharField(max_length=255, verbose_name=_("Name uz"))
    ru = models.CharField(max_length=255, verbose_name=_("Name ru"))
    coords = ArrayField(models.DecimalField(max_digits=16, decimal_places=10), verbose_name=_("Coordinates"))
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='children',  # This creates a reverse relation for the children of a Region
    )

    class Meta:
        db_table = 'regions'

    def __str__(self):
        return f"Region {self.id} - {self.uz} / {self.ru}"
