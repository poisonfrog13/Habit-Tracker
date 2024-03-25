import pytest

from django.contrib.auth.models import User
from pytest_factoryboy import register
from tests.factories import (
    UserFactory,
    HabitUnitFactory,
    HabitFactory,
    HabitRecordFactory,
)


register(UserFactory)
register(HabitUnitFactory)
register(HabitFactory)
register(HabitRecordFactory)

# ----------------- FOR HABIT TRACKER AND AUTHENTICATION


@pytest.fixture
def user_fixture(db, user_factory):
    user = user_factory.create()
    return user


@pytest.fixture
def habit_fixture(db, habit_factory):
    habit = habit_factory.create()
    return habit


@pytest.fixture
def habit_unit_fixture(db, habit_unit_factory):
    habit_unit = habit_unit_factory.create()
    return habit_unit


@pytest.fixture
def habit_record_fixture(db, habit_record_factory):
    record = habit_record_factory.create()
    return record


@pytest.fixture
def simulated_profile_fixture(
    db, user_factory, habit_factory, habit_unit_factory, habit_record_factory
):
    def create_profile(amount_habits=1, amount_records=1):
        user = user_factory.create()
        habits = habit_factory.create_batch(size=amount_habits, user=user)
        for habit in habits:
            habit_record_factory.create_batch(size=amount_records, habit=habit)
        return user

    return create_profile