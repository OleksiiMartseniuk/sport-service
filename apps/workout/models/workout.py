from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver

from apps.notification.service import SendNotification

from .category import Category


class Workout(models.Model):

    title = models.CharField(
        unique=True,
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


@receiver(pre_save, sender=Workout)
def change_publish(sender, instance: Workout, **kwargs):
    from apps.account.models import Profile

    if instance.id is not None:
        previous_workout = sender.objects.get(id=instance.id)
        if (
            instance.publish != previous_workout.publish and
            not instance.publish
        ):
            profiles = Profile.objects.filter(workout=instance)
            users_id = list(profiles.values_list('owner', flat=True))
            profiles.update(workout=None)
            SendNotification().send_notification_at_publish(
                users_id=users_id,
                workout_title=instance.title,
            )
