from django.db import models
from django.contrib.auth.models import User

from server.apps.habit_tracker import enums


# ----------------- CONSTANTS ----------------- #

CHOICES_TYPE = enums.HabitUnitType.as_django_choices()
CHOICES_NAME = enums.HabitUnitName.as_sorted_django_choices()

# ----------------- CONSTANTS ----------------- #


class HabitUnit(models.Model):
    class Meta:
        unique_together = ["name", "type"]

    name = models.CharField(
        max_length=30, null=False, blank=False, choices=CHOICES_NAME
    )
    type = models.CharField(
        max_length=20, null=False, blank=False, choices=CHOICES_TYPE
    )

    def __str__(self):
        return f"{self.name} = {self.type}"


class Habit(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    user = models.ForeignKey(
        User, related_name="habits", on_delete=models.CASCADE, null=False, blank=False
    )
    unit = models.ForeignKey(
        HabitUnit, on_delete=models.PROTECT, null=False, blank=False
    )

    def __str__(self):
        return f"{self.name}: {self.unit.name}"

    @property
    def records_all(self):
        return self.records.all()


class HabitRecord(models.Model):
    date = models.DateField(auto_now_add=True, null=False, blank=False)
    value = models.CharField(max_length=30, null=False, blank=False)
    habit = models.ForeignKey(
        Habit, related_name="records", on_delete=models.CASCADE, null=False, blank=False
    )

    def __str__(self):
        return (
            f"[{self.date}] - {self.habit.name}: {self.value} {self.habit.unit.name} "
        )
