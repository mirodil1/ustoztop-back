from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from parler.admin import TranslatableAdmin

from .models import Service


@admin.register(Service)
class ServiceAdmin(TranslatableAdmin):
    fieldsets = (
        (
            _("General"),
            {"fields": ("name", "description", "image", "price")},
        ),
    )
    list_display = [
        "name"    ]
    search_fields = [
        "name",
    ]
