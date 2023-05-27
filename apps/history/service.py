import logging

from django.contrib.auth.models import User
from django.utils import timezone

from apps.workout.models import Workout

from .models import WorkoutHistory

logger = logging.getLogger('db')


class HistoryAction:

    @staticmethod
    def create_workout(
        user: User,
        workout: Workout,
    ):
        detail_info = [
            {
                'datetime': f'{timezone.now().isoformat()}',
                'event': 'The program was started',
            },
        ]
        WorkoutHistory.objects.create(
            user=user,
            workout=workout,
            detail_info=detail_info,
        )

    @staticmethod
    def close_workout(
        user: User,
        workout: Workout,
    ):
        workout_history: WorkoutHistory | None = WorkoutHistory.objects.filter(
            user=user,
            workout=workout,
            data_close__isnull=True,
        ).first()

        if not workout_history:
            logger.error(
                'Not found history for close workout '
                f'filter(user={user.id}, workout={workout.id},'
                ' data_close__isnull=True)',
            )
            raise ValueError('Not found history for close workout')

        workout_history.close_workout()
