from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from apps.workout.models import Workout
from apps.utils.models import Event


class WorkoutHistory(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='history_workout',
    )
    workout = models.ForeignKey(
        Workout,
        on_delete=models.SET_NULL,
        related_name='history_workout',
        null=True,
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

    def close_workout(self):
        self.close_date = timezone.now()
        self.save(update_fields=('close_date',))

    def __str__(self) -> str:
        return (f"History [ {self.id} ] workout"
                f" user [ {self.user.username} ]")
