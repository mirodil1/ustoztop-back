from django.core.validators import FileExtensionValidator
from django.db import models
from django.template import defaultfilters
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from parler.models import TranslatableModel, TranslatedFields
from unidecode import unidecode

from apps.announcements.managers import CategoryManager
from apps.core.models import TimeStampedModel


class Category(TimeStampedModel, MPTTModel, TranslatableModel):
    """
    Category model
    """

    translations = TranslatedFields(
        name=models.CharField(max_length=255, db_index=True, verbose_name=_("Name")),
        slug=models.SlugField(
            max_length=255,
            db_index=True,
        ),
        meta={"unique_together": [("slug", "language_code")]},
    )
    icon = models.FileField(
        upload_to="category",
        null=True,
        blank=True,
        validators=[FileExtensionValidator(["svg", "png"])],
        verbose_name=_("Icon"),
    )
    parent = TreeForeignKey(
        "self",
        related_name="children",
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name=_("Parent category"),
    )

    order = models.PositiveIntegerField(
        default=0,
        blank=False,
        null=False,
    )

    objects = CategoryManager()

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
        db_table = "category"

    def save(self, *args, **kwargs):
        self.slug = defaultfilters.slugify(unidecode(self.name))
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class Announcement(TimeStampedModel):
    class LessonType(models.TextChoices):
        GROUP = "group", _("Group")
        INDIVIDUAL = "individual", _("Individual")

    class LessonPlace(models.TextChoices):
        ONLINE = "online", _("Online")
        IN_PERSON = "in_person", _("In Person")

    class LessonLanguage(models.TextChoices):
        UZ = "uz", _("Uzbek")
        RU = "ru", _("Russian")
        EN = "en", _("English")

    class LessonAudience(models.TextChoices):
        CHILDREN = "children", _("Children")
        ADULTS = "adults", _("Adults")
        ALL = "all", _("All")

    class AnnouncementStatus(models.TextChoices):
        ACTIVE = "active", _("Active")
        INACTICE = "inactive", _("Not active")
        WAITING = "waiting", _("Waiting")
        REJECTED = "rejected", _("Rejected")

    name = models.CharField(max_length=255, verbose_name=_("Name"))
    slug = models.SlugField(unique=True, verbose_name=_("Slug"))
    user_id = models.BigIntegerField(verbose_name=_("User ID"))
    phone_number = models.CharField(max_length=14, verbose_name=_("Phone number"))
    price = models.DecimalField(
        max_digits=14,
        decimal_places=2,
        verbose_name=_("Price"),
    )
    lessons_in_week = models.IntegerField(verbose_name=_("Lessons in a week"))
    lesson_duration_hours = models.IntegerField(verbose_name=_("Lesson duration"))
    lesson_type = models.CharField(
        max_length=10,
        choices=LessonType.choices,
        verbose_name=_("Lesson type"),
    )
    lesson_place = models.CharField(
        max_length=10,
        choices=LessonPlace.choices,
        verbose_name=_("Lesson place"),
    )
    lesson_language = models.CharField(
        max_length=2,
        choices=LessonLanguage.choices,
        verbose_name=_("Lesson language"),
    )
    lesson_audience = models.CharField(
        max_length=10,
        choices=LessonAudience.choices,
        null=True,
        blank=True,
        verbose_name=_("Lesson audience"),
    )
    status = models.CharField(
        max_length=20,
        choices=AnnouncementStatus.choices,
        default=AnnouncementStatus.WAITING,
        verbose_name=_("Status"),
    )
    description = models.TextField(verbose_name=_("Description"))
    is_active = models.BooleanField(
        default=False,
        verbose_name=_("Status"),
    )
    is_confirmed_by_admin = models.BooleanField(
        default=False,
        verbose_name=_("Admin confirmation"),
    )
    is_promoted = models.BooleanField(
        default=False,
        verbose_name=_("Promotion status"),
    )
    promotion_started = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Promotion start date"),
    )
    promotion_expired = models.DateField(
        null=True,
        blank=True,
        verbose_name=_("Promotion expire date"),
    )
    category = models.ForeignKey(
        to=Category,
        related_name="announcements",
        null=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        verbose_name = _("Announcement")
        verbose_name_plural = _("Announcements")
        db_table = "announcement"

    def __str__(self) -> str:
        return self.name
    