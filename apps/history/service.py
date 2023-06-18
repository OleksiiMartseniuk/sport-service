import logging

from django.contrib.auth.models import User
from django.utils import timezone

from apps.workout.models import Workout, Exercise
from apps.utils.models import Event

from .models import WorkoutHistory, ExerciseHistory
from .exceptions import WorkoutHistoryNotFound

logger = logging.getLogger('db')


class WorkoutHistoryAction:

    @staticmethod
    def create_workout(
        user: User,
        workout: Workout,
    ) -> None:
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
    ) -> None:
        history = self.get_current_workout_history(user=user, workout=workout)
        history.close_workout()
        # TODO: add close ExerciseHistory

    def close_workout_for_users(users_id: list[int], workout: Workout) -> None:
        WorkoutHistory.objects.filter(
            user__in=users_id,
            workout=workout,
            close_date__isnull=True,
        ).update(close_date=timezone.now())

    def update_workout_users(
        self,
        users_id: list[int],
        workout: Workout,
        # {'datetime': 'value', 'event': 'value'}
        detail_info: dict,
    ) -> None:
        history_list = WorkoutHistory.objects.filter(
            user__in=users_id,
            workout=workout,
            close_date__isnull=True,
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
            close_date__isnull=True,
        ).first()

        if not workout_history:
            logger.error(
                'Not found history for close workout '
                f'filter(user={user.id}, workout={workout.id},'
                ' close_date__isnull=True)',
            )
            raise WorkoutHistoryNotFound('Not found history for close workout')

        return workout_history


class ExerciseHistoryAction(WorkoutHistoryAction):

    def get_or_create(
        self,
        workout: Workout,
        user: User,
        exercise: Exercise,
    ) -> ExerciseHistory:
        workout_history = self.get_current_workout_history(
            workout=workout,
            user=user,
        )
        exercise_history, create = ExerciseHistory.objects.get_or_create(
            exercises_title=exercise.title,
            workout_title=workout.title,
            exercises=exercise,
            history_workout=workout_history,
            close_date=None,
        )
        if create:
            event = Event.objects.create(
                title='Вы начали выполнять программу тренировок',
            )
            exercise_history.event.add(event)
        return exercise_history
