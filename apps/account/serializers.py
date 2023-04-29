from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from django.contrib.auth.models import User

from .models import Profile


class MixinUserMeta:
    model = User
    fields = [
        'username',
        'email',
    ]
    extra_kwargs = {
        'username': {
            'required': False,
            'validators': [
                UniqueValidator(queryset=User.objects.all()),
            ],
        },
        'email': {
            'validators': [
                UniqueValidator(queryset=User.objects.all()),
            ],
        },
    }


class CreateUserSerializer(serializers.ModelSerializer):

    class Meta(MixinUserMeta):
        fields = [
            'username',
            'password',
            'email',
        ]
        write_only_fields = ['password']


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = [
            'reminder_time',
            'is_email',
        ]
        read_only_fields = ['is_email']


class UserSerializer(serializers.ModelSerializer):

    profile = ProfileSerializer()

    class Meta(MixinUserMeta):
        fields = [
            'username',
            'email',
            'profile',
        ]

    def update(self, instance: User, validated_data):
        for attr, value in validated_data.items():
            if isinstance(value, dict):
                for profile_attr, profile_value in value.items():
                    setattr(instance.profile, profile_attr, profile_value)
                continue
            setattr(instance, attr, value)

        instance.save()
        return instance
