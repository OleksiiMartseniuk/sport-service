from django.db import models
from django.contrib.auth.models import User

from .category import Category


class Workout(models.Model):

    title = models.CharField(
        max_length=255,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='workouts',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name='workouts',
        null=True,
    )
    publish = models.BooleanField(
        default=True,
    )
    created = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return self.title
