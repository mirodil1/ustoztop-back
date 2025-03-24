from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from parler.admin import TranslatableAdmin

from .models import Service, Slider


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
        "duration",
        "service_type",
        "service_audience",
        "price",
        "discount_price",
        "is_discount",
        "is_active",
    ]
    search_fields = [
        "name",
    ]



@admin.register(Slider)
class SliderAdmin(SortableAdminMixin, TranslatableAdmin):
    fieldsets = (
        (
            _("General"),
            {"fields": (
                "name",
                "link",
                "image_large",
                "image_medium",
                "is_active",
            )},
        ),
    )
    list_display = [
        "name",
        "is_active",
        "slider_order",
    ]
    ordering = ["slider_order"]
