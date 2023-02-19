from django.contrib.auth.models import User
from rest_framework import serializers

from .models import CustomUser


class UserValidateSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class UserCreateSerializer(UserValidateSerializer):
    def validate_user(self, username):
        try:
            CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            return username
        raise ValueError('User already exists')
