from rest_framework import serializers

from server.apps.habit_tracker.models import HabitUnit, Habit, HabitRecord
from server.apps.authentication.serializer import UserSerializer
from server.apps.core.serializers import DynamicFieldsModelSerializer




class CreateHabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = ("user", "name", "unit")


class HabitUnitSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = HabitUnit
        fields = ("id", "name", "type")


class RecordsSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = HabitRecord
        fields = ("id", "habit", "date", "value")

    id = serializers.IntegerField(required=False)
    date = serializers.DateField()
    value = serializers.CharField(max_length=30)


class HabitSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = Habit
        fields = ("id", "name", "user", "unit", "records")

    id = serializers.IntegerField(required=False)
    user = UserSerializer(fields=("id", "username"))
    name = serializers.CharField(max_length=50)
    unit = HabitUnitSerializer(fields=("id", "name", "type"))
    records = RecordsSerializer(
        many=True, fields=("id", "date", "value"), source="records_all"
    )
