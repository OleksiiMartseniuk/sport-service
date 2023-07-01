from rest_framework import serializers

from apps.utils.serializers import EventSerializer

from .models import WorkoutHistory

from apps.workout.serializers import WorkoutSmallSerializers
from apps.account.serializers import UserSmallSerializer


class WorkoutHistorySerializer(serializers.ModelSerializer):

    user = UserSmallSerializer(read_only=True)
    workout = WorkoutSmallSerializers(read_only=True)
    event = EventSerializer(many=True)

    class Meta:
        model = WorkoutHistory
        fields = '__all__'
