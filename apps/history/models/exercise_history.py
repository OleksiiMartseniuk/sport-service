from django.db import models
from django.utils import timezone

from apps.workout.models import Exercise
from apps.utils.models import Event

from ..models import WorkoutHistory


class ExerciseHistory(models.Model):

    # If exercises or workout removed save title
    exercises_title = models.CharField(
        max_length=255,
    )
    workout_title = models.CharField(
        max_length=255,
    )
    exercises = models.ForeignKey(
        Exercise,
        on_delete=models.SET_NULL,
        null=True,
    )
    history_workout = models.ForeignKey(
        WorkoutHistory,
        on_delete=models.CASCADE,
        related_name='exercise_history',
    )
    event = models.ManyToManyField(
        Event,
    )
    open_date = models.DateTimeField(
        auto_now_add=True,
    )
    close_date = models.DateTimeField(
        default=None,
        blank=True,
        null=True,
    )

    def close_exercise_history(self):
        self.close_date = timezone.now()
        self.save(update_fields=('close_date',))

    def __str__(self) -> str:
        return f'ExerciseHistory {self.id}'


class ExerciseApproaches(models.Model):

    exercise_history = models.ForeignKey(
        ExerciseHistory,
        on_delete=models.CASCADE,
        related_name='exercise_approaches',
    )
    current_approach = models.PositiveIntegerField()
    number_repetitions = models.PositiveIntegerField()
    created = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self) -> str:
        return (
            f'ExerciseApproaches {self.id} ExerciseHistory'
            f'{self.exercise_history.id}'
        )
