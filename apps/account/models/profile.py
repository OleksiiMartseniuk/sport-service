import logging

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from apps.workout.models import Workout
from apps.history.service import HistoryAction


logger = logging.getLogger('db')


class Profile(models.Model):

    MORNING = 9
    DAY = 14
    EVENING = 18

    ReminderTimeChoices = (
        (MORNING, 9),
        (DAY, 14),
        (EVENING, 18),
    )

    owner = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    reminder_time = models.IntegerField(
        choices=ReminderTimeChoices,
        blank=True,
        null=True,
    )
    workout = models.ForeignKey(
        Workout,
        on_delete=models.SET_NULL,
        related_name='profiles',
        blank=True,
        null=True,
    )

    def __str__(self) -> str:
        return self.owner.username


@receiver(post_save, sender=User)
def create_profile(sender, instance: User, created: bool, **kwargs):
    if created:
        Profile.objects.create(owner=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance: User, **kwargs):
    instance.profile.save()


@receiver(pre_save, sender=Profile)
def write_history_workout(sender, instance: Profile, **kwargs):
    if instance.id is not None:
        previous_profile: Profile = sender.objects.get(id=instance.id)
        if previous_profile.workout != instance.workout:
            if previous_profile.workout:
                HistoryAction.close_workout(
                    user=previous_profile.owner,
                    workout=previous_profile.workout,
                )
                logger.info(
                    f'User [{previous_profile.owner.id}] unsubscribed'
                    f' workout [{previous_profile.workout.id}]',
                )
            if instance.workout:
                HistoryAction.create_workout(
                    user=instance.owner,
                    workout=instance.workout,
                )
                logger.info(
                    f'User [{instance.owner.id}] subscribed'
                    f' to workout [{instance.workout.id}]',
                )
