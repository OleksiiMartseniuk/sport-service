from django.db import models
from django.utils import timezone
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
        on_delete=models.SET_NULL,
        related_name='history_workout',
        null=True,
    )
    # datetime - iso format
    # [{'datetime': 'value', 'event': 'value'}]
    detail_info = models.JSONField(default=list)
    data_open = models.DateTimeField(
        auto_now_add=True,
    )
    data_close = models.DateTimeField(
        default=None,
        blank=True,
        null=True,
    )

    def close_workout(self):
        self.data_close = timezone.now()
        self.save(update_fields=('data_close',))

    def __str__(self) -> str:
        return (f"History [ {self.id} ] workout"
                f" user [ {self.user.username} ]")
