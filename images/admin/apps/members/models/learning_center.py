from django.db import models


class DayOfWeek(models.TextChoices):
    MONDAY = "Mon", "Monday"
    TUESDAY = "Tue", "Tuesday"
    WEDNESDAY = "Wed", "Wednesday"
    THURSDAY = "Thu", "Thursday"
    FRIDAY = "Fri", "Friday"
    SATURDAY = "Sat", "Saturday"
    SUNDAY = "Sun", "Sunday"


# LearningCenter model
class LearningCenter(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    avatar = models.CharField(max_length=255, null=True, blank=True)
    banner = models.CharField(max_length=255, null=True, blank=True)

    user = models.ForeignKey("members.User", on_delete=models.CASCADE, related_name="learning_center")
    
    branch = models.ManyToManyField("Branch", related_name="learning_centers")
    working_schedule = models.ManyToManyField("WorkingSchedule", related_name="learning_centers")

    class Meta:
        unique_together = ("user",)  # Enforcing the unique user constraint


# Branch model
class Branch(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=255)

    learning_center = models.ForeignKey(LearningCenter, on_delete=models.CASCADE, related_name="branches")


# WorkingSchedule model
class WorkingSchedule(models.Model):
    id = models.BigIntegerField(primary_key=True)
    day_of_week = models.CharField(max_length=10, choices=DayOfWeek.choices)
    opening_time = models.TimeField(null=True, blank=True)
    closing_time = models.TimeField(null=True, blank=True)
    is_closed = models.BooleanField(default=False)

    learning_center = models.ForeignKey(LearningCenter, on_delete=models.CASCADE, related_name="working_schedules")

    class Meta:
        unique_together = ("learning_center", "day_of_week")
