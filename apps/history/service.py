from django.contrib.auth.models import User
from django.utils import timezone

from apps.workout.models import Workout

from .models import WorkoutHistory


class HistoryAction:

    @staticmethod
    def create_workout(
        user: User,
        workout: Workout,
        detail_info: str | None = None,
    ):
        if detail_info:
            detail_info = [{f'{timezone.now().isoformat()}': detail_info}]
        else:
            detail_info = []
        WorkoutHistory.objects.create(
            user=user,
            workout=workout,
            detail_info=detail_info,
        )
