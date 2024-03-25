from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from server.apps.habit_tracker.models import Habit, HabitRecord
from server.apps.habit_tracker.validators import (
    validate_habit_name,
    validate_habit_record_value,
)
from server.apps.habit_tracker.serializers import (
    HabitSerializer,
    CreateHabitSerializer,
    RecordsSerializer,
)


class HabitsList(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        habits = Habit.objects.filter(user=request.user)
        serializer = HabitSerializer(
            habits, many=True, fields=("id", "user", "name", "unit")
        )
        print(request.user)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK if habits else status.HTTP_204_NO_CONTENT,
        )

    def post(self, request, format=None):
        data = request.data.dict()
        data["user"] = request.user.pk
        serializer = CreateHabitSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, format=None):
        habits = Habit.objects.filter(user=request.user)
        habits.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class HabitDetail(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, habit_pk=None, format=None):
        try:
            habit = Habit.objects.get(pk=habit_pk, user=request.user)
        except Habit.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = HabitSerializer(habit)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, habit_pk=None, format=None):
        try:
            habit = Habit.objects.get(pk=habit_pk, user=request.user)
        except Habit.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        new_name = request.data.get("name", None)
        if validate_habit_name(new_name):
            habit.name = new_name
            habit.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, habit_pk=None, format=None):
        try:
            habit = Habit.objects.get(pk=habit_pk, user=request.user)
        except Habit.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        habit.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RecordsList(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, habit_pk=None, format=None):
        try:
            habit = Habit.objects.get(pk=habit_pk, user=request.user)
        except Habit.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = HabitSerializer(habit, fields=("id", "name", "unit", "records"))
        print(serializer.instance)
        return Response(serializer.data)

    def post(self, request, habit_pk=None, format=None):
        try:
            habit = Habit.objects.get(pk=habit_pk, user=request.user)
        except Habit.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        value = request.data.get("value", None)
        if validate_habit_record_value(value):
            record = HabitRecord(habit=habit, value=value)
            record.save()

            serializer_record = RecordsSerializer(record)
            return Response(serializer_record.data, status=status.HTTP_201_CREATED)

    def delete(self, request, habit_pk=None, format=None):
        try:
            habit = Habit.objects.get(pk=habit_pk, user=request.user)
        except Habit.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        records = HabitRecord.objects.filter(habit=habit)
        records.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RecordDetail(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, habit_pk=None, record_pk=None, format=None):
        try:
            record = HabitRecord.objects.get(habit__user=request.user, pk=record_pk)
        except HabitRecord.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = RecordsSerializer(record)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, habit_pk=None, record_pk=None, format=None):
        try:
            record = HabitRecord.objects.get(habit__user=request.user, pk=record_pk)
        except HabitRecord.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        new_value = request.data.get("value", None)
        if validate_habit_record_value(new_value):
            record.value = new_value
            record.save()
            serializer = RecordsSerializer(record)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def delete(self, request, habit_pk=None, record_pk=None, format=None):
        try:
            record = HabitRecord.objects.get(habit__user=request.user, pk=record_pk)
        except HabitRecord.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        record.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
