from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from mptt.admin import MPTTModelAdmin
from mptt.forms import MPTTAdminForm
from parler.admin import TranslatableAdmin
from parler.forms import TranslatableModelForm

from .models import Announcement, Category


class MyModelAdminForm(MPTTAdminForm, TranslatableModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["parent"].queryset = self.fields[
            "parent"
        ].queryset.prefetch_related("translations")


@admin.register(Category)
class CategoryAdmin(TranslatableAdmin, MPTTModelAdmin):
    fieldsets = (
        (
            _("General"),
            {"fields": ("name", "parent", "icon")},
        ),
    )
    list_display = [
        "order",
        "name",
        "parent",
        "icon_tag",
    ]
    search_fields = [
        "name",
    ]
    exclude = [
        "slug",
    ]

    @admin.display(description="Icon")
    def icon_tag(self, obj):
        return mark_safe(
            '<img src="%s" width="32" height="32" />'
            % (obj.icon.url if obj.icon else ""),
        )


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ["name"]
