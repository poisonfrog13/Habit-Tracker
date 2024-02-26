from django.contrib.auth.models import User
from rest_framework import serializers

from rest_framework.validators import UniqueValidator
from server.apps.authentication.validators import include_digit, include_upper_letter
from server.apps.habit_tracker.serializers import DynamicFieldsModelSerializer

class NewUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "email", "password")

    id = serializers.IntegerField(required=False)
    username = serializers.CharField(
        required=True,
        min_length=5,
        max_length=30,
        allow_blank=False,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(
        required=True,
        min_length=8,
        max_length=32,
        validators = [include_digit, include_upper_letter],
    )

class UserSerializer(DynamicFieldsModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "date_joined",
            "password",
        )
