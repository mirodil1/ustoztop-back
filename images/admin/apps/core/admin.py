from django.contrib import admin

from .models import Region

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ["uz"]
    search_fields = [
        "uz", "ru"
    ]
