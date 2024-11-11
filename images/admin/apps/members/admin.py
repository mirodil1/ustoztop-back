from django.contrib import admin

from .models import User, Tutor, LearningCenter


class MultiDBModelAdmin(admin.ModelAdmin):
    # A handy constant for the name of the alternate database.
    using = "members"

    def save_model(self, request, obj, form, change):
        # Tell Django to save objects to the 'members' database.
        obj.save(using=self.using)

    def delete_model(self, request, obj):
        # Tell Django to delete objects from the 'members' database
        obj.delete(using=self.using)

    def get_queryset(self, request):
        # Tell Django to look for objects on the 'members' database.
        return super().get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'members' database.
        return super().formfield_for_foreignkey(
            db_field, request, using=self.using, **kwargs
        )

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'members' database.
        return super().formfield_for_manytomany(
            db_field, request, using=self.using, **kwargs
        )


class MultiDBTabularInline(admin.StackedInline):
    using = "members"

    def get_queryset(self, request):
        # Tell Django to look for inline objects on the 'members' database.
        return super().get_queryset(request).using(self.using)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Tell Django to populate ForeignKey widgets using a query
        # on the 'members' database.
        return super().formfield_for_foreignkey(
            db_field, request, using=self.using, **kwargs
        )

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        # Tell Django to populate ManyToMany widgets using a query
        # on the 'members' database.
        return super().formfield_for_manytomany(
            db_field, request, using=self.using, **kwargs
        )


class TutorInline(MultiDBTabularInline):
    model = Tutor
    readonly_fields = [
        "id",
        "first_name",
        "last_name",
        "description",
        "avatar",
        "gender"
    ]
    can_delete = False
    verbose_name = "Tutor"
    verbose_name_plural = "Tutor"


class LearningCenterInline(MultiDBTabularInline):
    model = LearningCenter
    readonly_fields = [
        "id",
        "name",
        "description",
        "avatar",
        "banner",
    ]
    can_delete = False
    verbose_name = "Learning Center"
    verbose_name_plural = "Learning Center"



@admin.register(User)
class MemberAdmin(MultiDBModelAdmin):
    list_display = [
        "id",
        "phone_number",
        "is_active",
        "is_verified_by_admin",
        "is_premium",
    ]
    inlines = [LearningCenterInline, TutorInline]
    readonly_fields = [
        "password",
        "id",
        "phone_number",
        "web_link",
        "insta_link",
        "facebook_link",
        "email",
        "telegram_link",
        "location_id",
    ]

    def get_inlines(self, request, obj):
        for role in obj.roles.all():
            if role.role_name == "learning_center":
                return [LearningCenterInline]
            elif role.role_name == "tutor":
                return [TutorInline]
        return []
