from django.db import models

from apps.workout.utils import exercise_image_path
from .workout import Workout


class Exercise(models.Model):

    MONDAY = 'Mun'
    TUESDAY = 'Tues'
    WEDNESDAY = 'Wed'
    THURSDAY = 'Thurs'
    FRIDAY = 'Fri'
    SATURDAY = 'Sat'
    SUNDAY = 'Sun'

    DAY_WEEK = (
        (MONDAY, 'Monday'),
        (TUESDAY, 'Tuesday'),
        (WEDNESDAY, 'Wednesday'),
        (THURSDAY, 'Thursday'),
        (FRIDAY, 'Friday'),
        (SATURDAY, 'Saturday'),
        (SUNDAY, 'Sunday'),
    )

    title = models.CharField(
        max_length=255,
    )
    workout = models.ForeignKey(
        Workout,
        on_delete=models.CASCADE,
        related_name='exercises',
    )
    number_approaches = models.PositiveIntegerField()
    number_repetitions = models.PositiveIntegerField()
    rest_second = models.PositiveIntegerField()
    day = models.CharField(
        max_length=10,
        choices=DAY_WEEK,
    )
    image = models.ImageField(
        upload_to=exercise_image_path,
    )
    publish = models.BooleanField(
        default=True,
    )
    created = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return f'Exercise [{self.title}] Workout [{self.workout.title}]'
