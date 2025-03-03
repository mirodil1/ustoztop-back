import uuid

from django.db.models import Manager
from django.db import models
from django.utils import timezone


class MembersManager(Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).using("members")

    def delete(self, *args, **kwargs):
        return super().delete(*args, **kwargs).using("members")


# LoginHistoryRecord model
class LoginHistoryRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    device = models.ForeignKey("Device", on_delete=models.CASCADE)
    login_date = models.DateTimeField(default=timezone.now)
    device_type = models.CharField(max_length=255, default="web")

    class Meta:
        unique_together = ["id", "device_type"]
        db_table = "login_history"
        base_manager_name = 'objects'
        default_manager_name = 'objects'

    def __str__(self):
        return f"<LoginHistoryRecord user={self.user.id} device={self.device.id} date={self.login_date}>"

    def delete(self, using=None, keep_parents=False):
        using = using or "members"  # Force deletion in "members"
        super().delete(using=using, keep_parents=keep_parents)

    objects = MembersManager()

# Device model
class Device(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey("User", on_delete=models.SET_NULL, null=True)
    user_agent = models.TextField()

    class Meta:
        db_table = "devices"
        base_manager_name = 'objects'
        default_manager_name = 'objects'

    def __str__(self):
        return f"<Device id={self.id}, user_id={self.user.id}>"

    objects = MembersManager()

# UserRoleAssociation (many-to-many) model
class UserRoleAssociation(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    role = models.ForeignKey("Role", on_delete=models.CASCADE)

    class Meta:
        unique_together = ["user", "role"]
        db_table = "user_role_association"


# Role model
class Role(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role_name = models.CharField(max_length=255, unique=True)
    # users = models.ManyToManyField("User", through=UserRoleAssociation, related_name="roles")

    class Meta:
        db_table = "roles"


# Wallet model
class Wallet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    balance = models.FloatField(default=0.0)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "wallets"

    def __str__(self):
        return f"<Wallet(id={self.id}, user_id={self.user.id}, balance={self.balance})>"


# Location model
class Location(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    longitude = models.FloatField()
    latitude = models.FloatField()

    class Meta:
        db_table = "locations"


class UserTag(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='tags', to_field='id')
    category_id = models.IntegerField(null=True)
    
    class Meta:
        db_table = 'user_tags'
        unique_together = ('user', 'category_id')

    def __str__(self):
        return f"{self.user} - {self.category_id}"


# User model (including relationships)
class User(models.Model):
    id = models.BigIntegerField(primary_key=True)
    phone_number = models.CharField(max_length=14, unique=True)
    email = models.EmailField(max_length=255, unique=True, null=True, blank=True)
    password = models.CharField(max_length=255)
    web_link = models.CharField(max_length=255, null=True, blank=True)
    insta_link = models.CharField(max_length=255, null=True, blank=True)
    facebook_link = models.CharField(max_length=255, null=True, blank=True)
    telegram_link = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_verified_by_admin = models.BooleanField(default=False)
    is_premium = models.BooleanField(default=False)
    premium_started = models.DateField(null=True, blank=True)
    premium_expired = models.DateField(null=True, blank=True)

    roles = models.ManyToManyField("Role", through=UserRoleAssociation, related_name="users")
    location_id = models.UUIDField(null=True)

    class Meta:
        db_table = "users"
        app_label = "members"
        base_manager_name = 'objects'
        default_manager_name = 'objects'


    def __str__(self):
        return self.phone_number

    objects = MembersManager()
