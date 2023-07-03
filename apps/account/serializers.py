from rest_framework import serializers

from django.contrib.auth.models import User

from djoser.serializers import UserSerializer
from djoser.conf import settings

from .models import Profile


class UserSmallSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'id',
            'username',
        ]


class UserCustomSerializer(UserSerializer):
    class Meta:
        model = User
        fields = tuple(User.REQUIRED_FIELDS) + (
            settings.USER_ID_FIELD,
            settings.LOGIN_FIELD,
            'is_staff',
        )
        read_only_fields = (settings.LOGIN_FIELD, 'is_staff')


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = [
            'reminder_time',
            'workout',
        ]
