import uuid

from django.db import models
from django.utils import timezone


class Gender(models.TextChoices):
    MALE = "M", "Male"
    FEMALE = "F", "Female"
    OTHER = "O", "Other"


class LanguageLevel(models.TextChoices):
    BEGINNER = "Beginner", "Beginner"
    INTERMEDIATE = "Intermediate", "Intermediate"
    ADVANCED = "Advanced", "Advanced"


class EducationDegree(models.TextChoices):
    BACHELOR = "Bachelor", "Bachelor"
    MASTER = "Master", "Master"
    PHD = "PhD", "PhD"


# Tutor model
class Tutor(models.Model):
    id = models.BigIntegerField(primary_key=True)
    first_name = models.CharField(max_length=64, null=True, blank=True)
    last_name = models.CharField(max_length=64, null=True, blank=True)
    gender = models.CharField(max_length=1, choices=Gender.choices, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    avatar = models.CharField(max_length=255, null=True, blank=True)
    user = models.OneToOneField("members.User", on_delete=models.CASCADE, related_name="tutor")
    # language = models.ForeignKey("Language", related_name="tutors", blank=True, on_delete=models.CASCADE)
    # education = models.ForeignKey("Education", related_name="tutors", blank=True, on_delete=models.CASCADE)
    # experience = models.ForeignKey("Experience", related_name="tutors", blank=True, on_delete=models.CASCADE)

    class Meta:
        db_table = "tutor"


# Language model
class Language(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=64)
    level = models.CharField(max_length=20, choices=LanguageLevel.choices)
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name="languages")

    class Meta:
        db_table = "language"


# Education model
class Education(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    degree = models.CharField(max_length=10, choices=EducationDegree.choices)
    field_of_study = models.CharField(max_length=255)
    start_year = models.DateField(null=True, blank=True)
    finish_year = models.DateField(null=True, blank=True)
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name="educations")

    class Meta:
        db_table = "education"


# Experience model
class Experience(models.Model):
    id = models.BigIntegerField(primary_key=True)
    organization = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    start_year = models.DateField()
    finish_year = models.DateField(null=True, blank=True)
    is_working = models.BooleanField(default=False)

    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name="experiences")

    class Meta:
        db_table = "experience"