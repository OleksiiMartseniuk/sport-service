from rest_framework import serializers

from apps.utils.serializers import EventSerializer

from .models import WorkoutHistory

from apps.workout.serializers import (
    WorkoutSmallSerializers,
    WorkoutRetrieveSerializers,
)
from apps.account.serializers import UserSmallSerializer, UserCustomSerializer


class WorkoutHistorySerializer(serializers.ModelSerializer):

    user = UserSmallSerializer(read_only=True)
    workout = WorkoutSmallSerializers(read_only=True)
    event = EventSerializer(many=True)

    class Meta:
        model = WorkoutHistory
        fields = '__all__'


class WorkoutHistoryRetrieveSerializer(serializers.ModelSerializer):

    user = UserCustomSerializer(read_only=True)
    workout = WorkoutRetrieveSerializers(read_only=True)
    event = EventSerializer(
        many=True,
        read_only=True,
    )
    exercise_history = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True,
    )

    class Meta:
        model = WorkoutHistory
        fields = '__all__'
