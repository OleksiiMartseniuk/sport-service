import logging

from django.contrib.auth.models import User
from django.utils import timezone

from apps.workout.models import Workout

from .models import WorkoutHistory
from .exceptions import HistoryWorkoutNotFound

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

    def close_workout(
        self,
        user: User,
        workout: Workout,
    ):
        history = self.get_current_workout_history(user=user, workout=workout)
        history.close_workout()

    def update_workout(
        self,
        user: User,
        workout: Workout,
        # {'datetime': 'value', 'event': 'value'}
        detail_info: dict,
    ):
        history = self.get_current_workout_history(user=user, workout=workout)
        history.detail_info.append(detail_info)
        history.save()

    @staticmethod
    def get_current_workout_history(
        user: User,
        workout: Workout,
    ) -> WorkoutHistory:
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
            raise HistoryWorkoutNotFound('Not found history for close workout')

        return workout_history
