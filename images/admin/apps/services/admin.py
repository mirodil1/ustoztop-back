from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from parler.admin import TranslatableAdmin

from .models import Service


@admin.register(Service)
class ServiceAdmin(TranslatableAdmin):
    fieldsets = (
        (
            _("General"),
            {"fields": (
                "name",
                "description",
                "image",
                "price",
                "duration",
                "discount_price",
                "service_audience",
                "service_type",
                "is_discount",
                "is_active",
            )},
        ),
    )
    list_display = [
        "name",
        "is_discount",
        "is_active",
    ]
    search_fields = [
        "name",
    ]
