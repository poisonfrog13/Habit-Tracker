import datetime
import random
from enum import unique
import factory
from faker import Faker

from django.contrib.auth.models import User

from server.apps.habit_tracker import enums
from server.apps.habit_tracker import models


fake = Faker()
# ----------------- CONSTANTS ----------------- #

CHOICES_TYPE = enums.HabitUnitType.as_django_choices()
CHOICES_NAME = enums.HabitUnitName.as_sorted_django_choices()

# ----------------- CONSTANTS ----------------- #


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("name")
    email = factory.Faker("ascii_email")
    password = "password"
    is_active = "True"
    is_staff = "False"


class HabitUnitFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.HabitUnit
        django_get_or_create = ("name", "type")

    name = factory.Iterator(CHOICES_NAME)
    type = factory.Iterator(CHOICES_TYPE)


class HabitFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Habit

    name = factory.LazyFunction(
        lambda: random.choice(
            ["Coding", "Swimming", "Cold Shower", "Reading", "Dancing"]
        )
    )
    user = factory.SubFactory(UserFactory)
    unit = factory.SubFactory(HabitUnitFactory)


class HabitRecordFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.HabitRecord

    date = factory.Faker("date")
    value = "somevalue"
    habit = factory.SubFactory(HabitFactory)