import pytest

from django.contrib.auth.models import User

from server.apps.habit_tracker import models


# ------------------ CREATE


def test_new_user(db, user_factory):
    # Given
    init_count = User.objects.all().count()
    expected_count = init_count + 1

    # When
    user = user_factory.create()
    found_count = User.objects.all().count()

    # Then
    assert expected_count == found_count


def test_new_habit(db, habit_factory):
    # Given
    init_count = models.Habit.objects.all().count()
    expected_count = init_count + 1

    # When
    habit = habit_factory.create()
    found_count = models.Habit.objects.all().count()

    # Then
    assert expected_count == found_count


def test_new_habit_unit(db, habit_unit_factory):
    # Given
    init_count = models.HabitUnit.objects.all().count()
    expected_count = init_count + 1

    # When
    habit_unit = habit_unit_factory.create()
    found_count = models.HabitUnit.objects.all().count()

    # Then
    assert expected_count == found_count


def test_new_habit_record(db, habit_record_factory):
    # Given
    init_count = models.HabitRecord.objects.all().count()
    expected_count = init_count + 1

    # When
    record = habit_record_factory.create()
    found_count = models.HabitRecord.objects.all().count()

    # Then
    assert expected_count == found_count


# ------------------ UPDATE


def test_habit_name_update(db, habit_factory):
    # Given
    habit = habit_factory.create()
    init_name = habit.name

    # When
    habit.name = "NEWNAME"
    habit.save()
    updated_habit = models.Habit.objects.get(pk=habit.pk)

    new_name = updated_habit.name

    # Then
    assert new_name != init_name


def test_habit_record_value(db, habit_record_factory):
    # Given
    record = habit_record_factory.create()
    init_value = record.value

    # When
    record.value = "THISISNEWVALUE"
    record.save()
    updated_record = models.HabitRecord.objects.get(pk=record.pk)
    new_value = updated_record.value

    # Then
    assert new_value != init_value


# ------------------ DELETE

# Separated objects


def test_user_delete(user_fixture):
    # Given
    init_count = User.objects.all().count()
    expected_count = init_count - 1

    # When
    user_fixture.delete()
    found_count = User.objects.all().count()

    # Then
    assert expected_count == found_count


def test_habit_delete(habit_fixture):
    # Given
    init_count = models.Habit.objects.all().count()
    expected_count = init_count - 1

    # When
    habit_fixture.delete()
    found_count = models.Habit.objects.all().count()

    # Then
    assert expected_count == found_count


def test_habit_record_delete(habit_record_fixture):
    # Given
    init_count = models.HabitRecord.objects.all().count()
    expected_count = init_count - 1

    # When
    habit_record_fixture.delete()
    found_count = models.HabitRecord.objects.all().count()

    # Then
    assert expected_count == found_count


# Mixed objects


def test_user_habit_delete(db, user_fixture, habit_factory):
    # Given
    habit = habit_factory.create(user=user_fixture)
    habit_table = models.Habit.objects.filter(pk=habit.pk)
    init_table_valid = habit_table.exists()

    # When
    User.objects.all().delete()
    habit_table = models.Habit.objects.filter(pk=habit.pk)
    found_table_valid = habit_table.exists()

    # Then
    assert found_table_valid != init_table_valid


def test_habit_record_delete(db, habit_fixture, habit_record_factory):
    # Given
    record = habit_record_factory.create(habit=habit_fixture)
    record_table = models.HabitRecord.objects.filter(pk=record.pk)
    init_table_valid = record_table.exists()

    # When
    models.Habit.objects.all().delete()
    record_table = models.HabitRecord.objects.filter(pk=record.pk)
    found_table_valid = record_table.exists()

    # Then
    assert found_table_valid != init_table_valid