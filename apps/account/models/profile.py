from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):

    MORNING = 9
    DAY = 14
    EVENING = 18

    ReminderTimeChoices = (
        (MORNING, 9),
        (DAY, 14),
        (EVENING, 18),
    )

    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    reminder_time = models.IntegerField(
        choices=ReminderTimeChoices,
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
