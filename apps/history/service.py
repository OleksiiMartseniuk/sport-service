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
                'event': f'The program #{workout.title} was started',
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

    def close_workout_for_users(users_id: list[int], workout: Workout):
        WorkoutHistory.objects.filter(
            user__in=users_id,
            workout=workout,
            data_close__isnull=True,
        ).update(data_close=timezone.now())

    def update_workout_users(
        self,
        users_id: list[int],
        workout: Workout,
        # {'datetime': 'value', 'event': 'value'}
        detail_info: dict,
    ):
        history_list = WorkoutHistory.objects.filter(
            user__in=users_id,
            workout=workout,
            data_close__isnull=True,
        ).only('detail_info')

        for history in history_list:
            history.detail_info.append(detail_info)
            history.save(update_fields=('detail_info',))

    @staticmethod
    def get_current_workout_history(
        user: User,
        workout: Workout,
    ) -> WorkoutHistory:
        workout_history = WorkoutHistory.objects.filter(
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
