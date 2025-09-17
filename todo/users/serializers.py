from sqlite3 import IntegrityError
from django.db import transaction
from rest_framework import serializers, status
from rest_framework.exceptions import APIException

from .models import User


class Conflict(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "Conflict."
    default_code = "conflict"


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["id", "email", "password"]

    def create(self, validated_data):
        try:
            with transaction.atomic():
                user = User(email=validated_data["email"])
                user.set_password(validated_data["password"])
                user.save()
                return user
        except IntegrityError:
            raise Conflict("Email already exists.")
