from django.contrib import admin

from .models import Region

class RegionInline(admin.StackedInline):
    model = Region
    extra = 10


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ["uz", "children_count"]
    search_fields = [
        "uz", "ru"
    ]
    inlines = [RegionInline]

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(parent__isnull=True)

    @admin.display(description="Children")
    def children_count(self, obj):
        count = obj.children.count()
        return count