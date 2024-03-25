from mimetypes import init
import pytest
import json
import datetime

from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from server.apps.habit_tracker.api import (
    URL_NAME__HABIT_RECORDS,
    URL_NAME__HABITS_LIST,
    URL_NAME__HABITS_ONE,
    URL_NAME__RECORD_ONE,
)


# ----------------- CONSTANTS ----------------- #

AMOUNT_HABITS = 10
AMOUNT_RECORDS = 5

# ----------------- CONSTANTS ----------------- #


def auth_token(simulated_user):
    """To call this function every time, when we need a token.
    To parse a fixture simulated_profile as an argument"""

    token, _ = Token.objects.update_or_create(user=simulated_user)
    return {"Authorization": f"Token {token.key}"}


# ----------------- API's
def test_api_non_auth(db, client, simulated_profile_fixture):
    # Given
    user = simulated_profile_fixture(amount_habits=5, amount_records=10)

    # When + Then
    assert client.get("/api/habits/").status_code == 403
    assert client.get("/api/habits/1/").status_code == 403
    assert client.get("/api/habits/1/records/").status_code == 403
    assert client.get("/api/habits/1/records/1/").status_code == 403


def test_api__habits_list(db, client, simulated_profile_fixture):
    # Given

    # User with habits
    user = simulated_profile_fixture(
        amount_habits=AMOUNT_HABITS, amount_records=AMOUNT_RECORDS
    )

    expected_habit_count = AMOUNT_HABITS
    expected_records_habit = AMOUNT_HABITS * AMOUNT_RECORDS

    found_habits_count = user.habits.all().count()
    habits = user.habits.all()
    found_records_count = sum([habit.records.all().count() for habit in habits])

    # User with empty habit's list
    amount_no_habits = 0
    amount_no_records = 0

    user_no_habit = simulated_profile_fixture(
        amount_habits=amount_no_habits, amount_records=amount_no_records
    )

    found_no_habits_count = user_no_habit.habits.all().count()
    habits = user_no_habit.habits.all()
    found_no_records_count = sum([habit.records.all().count() for habit in habits])

    # When
    response = client.get(reverse(URL_NAME__HABITS_LIST), headers=auth_token(user))
    response_no_habit = client.get(
        reverse(URL_NAME__HABITS_LIST), headers=auth_token(user_no_habit)
    )

    # Then
    assert response.status_code == 200
    assert response_no_habit.status_code == 204
    assert expected_habit_count == found_habits_count
    assert expected_records_habit == found_records_count
    assert expected_habit_count != found_no_habits_count
    assert expected_records_habit != found_no_records_count


def test_api__habits_create(db, client, simulated_profile_fixture, habit_unit_fixture):
    # Given
    user = simulated_profile_fixture(
        amount_habits=AMOUNT_HABITS, amount_records=AMOUNT_RECORDS
    )
    habits = user.habits.all()
    init_habits_count = habits.count()

    expected_habit_count = init_habits_count + 1

    new_habit = {"name": "writing tests", "unit": habit_unit_fixture.pk}

    # Use with invalid data
    user_invalid_data = simulated_profile_fixture(
        amount_habits=AMOUNT_HABITS, amount_records=AMOUNT_RECORDS
    )
    bad_data_habit = {
        "name": 12311111111111111111111111111111111111111111111111111111111,
        "unit": 1,
    }

    # When
    response = client.post(
        reverse(URL_NAME__HABITS_LIST), data=new_habit, headers=auth_token(user)
    )
    response_invalid_data = client.post(
        reverse(URL_NAME__HABITS_LIST),
        data=bad_data_habit,
        headers=auth_token(user_invalid_data),
    )
    found_habits_count = habits.count()

    # Then
    assert response.status_code == 201, response.content
    assert response_invalid_data.status_code == 400, response.content
    assert expected_habit_count == found_habits_count


def test_api__habits_delete(db, client, simulated_profile_fixture):
    # Given
    user = simulated_profile_fixture(amount_habits=AMOUNT_HABITS)
    habits = user.habits.all()
    init_count = habits.count()

    expected_count = init_count - AMOUNT_HABITS

    # When
    response = client.delete(reverse(URL_NAME__HABITS_LIST), headers=auth_token(user))
    found_count = user.habits.all().count()

    # Then
    assert response.status_code == 204
    assert expected_count == found_count


def test_api__habit_detail_read(db, client, simulated_profile_fixture):
    # Given
    user = simulated_profile_fixture(
        amount_habits=AMOUNT_HABITS, amount_records=AMOUNT_RECORDS
    )
    habit_1 = user.habits.first()
    habit_pk = {"habit_pk": habit_1.pk}
    habit_pk_404 = {"habit_pk": 1000}

    # When
    response = client.get(
        reverse(URL_NAME__HABITS_ONE, kwargs=habit_pk), headers=auth_token(user)
    )
    response_404 = client.get(
        reverse(URL_NAME__HABITS_ONE, kwargs=habit_pk_404), headers=auth_token(user)
    )

    # Then
    assert response.status_code == 200
    assert response_404.status_code == 404


def test_api__habit_detail_update(db, client, simulated_profile_fixture):
    # Given
    user = simulated_profile_fixture(amount_habits=AMOUNT_HABITS)
    habit = user.habits.first()
    init_habit_name = habit.name
    habit_pk = {"habit_pk": habit.pk}
    new_habit_name = {"name": "Cookin"}
    token = auth_token(user)
    token["Content-Type"] = "application/json"

    # When
    response = client.put(
        reverse(URL_NAME__HABITS_ONE, kwargs=habit_pk),
        data=json.dumps(new_habit_name),
        headers=token,
    )

    habit.refresh_from_db()
    found_habit_name = habit.name

    # Then
    assert response.status_code == 200, response.content
    assert found_habit_name != init_habit_name


def test_api__habit_detail_delete(db, client, simulated_profile_fixture) -> None:
    # Given
    user = simulated_profile_fixture(amount_habits=AMOUNT_HABITS)
    habits = user.habits.all()
    init_habits_count = habits.count()
    habit = user.habits.first()
    habit_pk = {"habit_pk": habit.pk}

    expected_count = init_habits_count - 1

    # When
    response = client.delete(
        reverse(URL_NAME__HABITS_ONE, kwargs=habit_pk), headers=auth_token(user)
    )
    found_count = habits.count()

    # Then
    assert response.status_code == 204
    assert expected_count == found_count


def test_api__records_list(db, client, simulated_profile_fixture):
    # Given
    user = simulated_profile_fixture(
        amount_habits=AMOUNT_HABITS, amount_records=AMOUNT_RECORDS
    )
    habit = user.habits.first()
    habit_pk = {"habit_pk": habit.pk}
    records_count = habit.records.count()

    expected_count = records_count

    # When
    response = client.get(
        reverse(URL_NAME__HABIT_RECORDS, kwargs=habit_pk), headers=auth_token(user)
    )
    data = json.loads(response.content)
    found_count = len(data["records"])

    # Then
    assert response.status_code == 200
    assert expected_count == found_count


def test_api__records_create(db, client, simulated_profile_fixture):
    # Given
    user = simulated_profile_fixture(
        amount_habits=AMOUNT_HABITS, amount_records=AMOUNT_RECORDS
    )
    habit = user.habits.first()
    init_records_count = habit.records.count()
    expected_count = init_records_count + 1

    habit_pk = {"habit_pk": habit.pk}
    new_record = {"date": datetime.datetime.now(), "value": "20", "habit": habit.pk}

    habit_invalid_pk = {"habit_pk": 23266}
    invalid_data_record = {"date": "llll", "value": "20", "habit": 23266}

    # When
    response = client.post(
        reverse(URL_NAME__HABIT_RECORDS, kwargs=habit_pk),
        data=new_record,
        headers=auth_token(user),
    )
    response_404 = client.post(
        reverse(URL_NAME__HABIT_RECORDS, kwargs=habit_invalid_pk),
        data=invalid_data_record,
        headers=auth_token(user),
    )
    habit.refresh_from_db()
    found_count = habit.records.count()

    # Then
    assert response.status_code == 201
    assert response_404.status_code == 404
    assert expected_count == found_count


def test_api__records_delete(db, client, simulated_profile_fixture):
    # Given
    user = simulated_profile_fixture(
        amount_habits=AMOUNT_HABITS, amount_records=AMOUNT_RECORDS
    )
    habit = user.habits.first()
    init_records_count = habit.records.count()
    expected_count = init_records_count - AMOUNT_RECORDS

    habit_pk = {"habit_pk": habit.pk}

    # When
    response = client.delete(
        reverse(URL_NAME__HABIT_RECORDS, kwargs=habit_pk), headers=auth_token(user)
    )
    habit.refresh_from_db()
    found_count = habit.records.count()

    # Then
    assert response.status_code == 204
    assert expected_count == found_count


def test_api__records_detail_read(db, client, simulated_profile_fixture):
    # Given
    user = simulated_profile_fixture(
        amount_habits=AMOUNT_HABITS, amount_records=AMOUNT_RECORDS
    )
    habit = user.habits.first()
    record = habit.records.first()

    habits_record_pk = {"habit_pk": habit.pk, "record_pk": record.pk}
    invalid_habits_record_pk = {"habit_pk": habit.pk, "record_pk": 6000}

    # When
    response = client.get(
        reverse(URL_NAME__RECORD_ONE, kwargs=habits_record_pk), headers=auth_token(user)
    )
    response_404 = client.get(
        reverse(URL_NAME__RECORD_ONE, kwargs=invalid_habits_record_pk),
        headers=auth_token(user),
    )

    # Then
    assert response.status_code == 200
    assert response_404.status_code == 404


def test_api__records_detail_update(db, client, simulated_profile_fixture):
    # Given
    user = simulated_profile_fixture(
        amount_habits=AMOUNT_HABITS, amount_records=AMOUNT_RECORDS
    )
    habit = user.habits.first()
    record = habit.records.first()
    init_value = record.value
    habits_record_pk = {"habit_pk": habit.pk, "record_pk": record.pk}

    new_value = {"value": "Updated in TEST value"}
    token = auth_token(user)
    token["Content-Type"] = "application/json"

    # When
    response = client.put(
        reverse(URL_NAME__RECORD_ONE, kwargs=habits_record_pk),
        data=json.dumps(new_value),
        headers=token,
    )
    record.refresh_from_db()
    found_value = record.value

    # Then
    assert response.status_code == 202
    assert found_value != init_value


def test_api__records_detail_delete(db, client, simulated_profile_fixture):
    # Given
    user = simulated_profile_fixture(
        amount_habits=AMOUNT_HABITS, amount_records=AMOUNT_RECORDS
    )
    habit = user.habits.first()
    record = habit.records.first()
    init_count_records = habit.records.all().count()
    init_count_habits = user.habits.all().count()
    expected_count = init_count_records - 1

    habits_record_pk = {"habit_pk": habit.pk, "record_pk": record.pk}

    # When
    response = client.delete(
        reverse(URL_NAME__RECORD_ONE, kwargs=habits_record_pk), headers=auth_token(user)
    )
    found_count_records = habit.records.all().count()
    found_count_habits = user.habits.all().count()
    
    # Then
    assert response.status_code == 204, response.content
    assert expected_count == found_count_records
    assert found_count_habits == init_count_habits