from adminsortable2.admin import SortableAdminMixin, SortableStackedInline
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from mptt.admin import MPTTModelAdmin
from mptt.forms import MPTTAdminForm
from parler.admin import TranslatableAdmin, TranslatableStackedInline
from parler.forms import TranslatableModelForm

from .models import Announcement, Category, Location


class MyModelAdminForm(MPTTAdminForm, TranslatableModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["parent"].queryset = self.fields[
            "parent"
        ].queryset.prefetch_related("translations")


class CategoryChildInline(SortableStackedInline, TranslatableStackedInline):
    model = Category
    exclude = ["slug"]
    fieldsets = (
        (
            _("General"),
            {"fields": ("name", "parent", "order")},
        ),
    )
    ordering = ["order",]
    extra = 10


@admin.register(Category)
class CategoryAdmin(SortableAdminMixin, TranslatableAdmin, MPTTModelAdmin):
    fieldsets = (
        (
            _("General"),
            {"fields": ("name", "parent", "icon")},
        ),
    )
    list_display = [
        "name",
        "children_count",
        "icon_tag",
        "order",

    ]
    search_fields = [
        "name",
    ]
    exclude = [
        "slug",
    ]
    ordering = ["order",]
    inlines = [CategoryChildInline]
    form = MyModelAdminForm
    
    @admin.display(description="Icon")
    def icon_tag(self, obj):
        return mark_safe(
            '<img src="%s" width="32" height="32" />'
            % (obj.icon.url if obj.icon else ""),
        )
    
    @admin.display(description="Children")
    def children_count(self, obj):
        count = obj.children.count()
        return count

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(parent=None)

@admin.register(Location)
class LocationInline(admin.ModelAdmin):
    pass


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ["name", "status"]
    exclude = [
        "is_active",
        "is_confirmed_by_admin",
    ]
    readonly_fields = ["location"]
    # inlines = [LocationInline]
