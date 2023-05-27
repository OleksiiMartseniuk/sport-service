from django.db import models
from django.contrib.auth.models import User

from apps.workout.models import Workout


class WorkoutHistory(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='history_workout',
    )
    workout = models.ForeignKey(
        Workout,
        on_delete=models.CASCADE,
        related_name='history_workout',
    )
    # datetime - iso format
    # [{'datetime': 'event'}]
    detail_info = models.JSONField(default=list)
    data_open = models.DateTimeField(
        auto_now_add=True,
    )
    data_close = models.DateTimeField(
        default=None,
        blank=True,
        null=True,
    )

    def __str__(self) -> str:
        return (f"History workout [ {self.workout.title} ]"
                f" user [ {self.user.username} ]")
