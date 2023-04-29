from django.db import models
from django.contrib.auth.models import User


class Notification(models.Model):

    CREATE = 'create'
    SUCCESS = 'success'
    ERROR = 'error'
    StatusChoices = (
        (CREATE, 'create'),
        (SUCCESS, 'success'),
        (ERROR, 'error'),
    )

    AUTH = 'auth'
    REMINDER = 'reminder'
    GroupNotificationChoices = (
        (AUTH, 'auth'),
        (REMINDER, 'reminder'),
    )

    user = models.ForeignKey(
        User,
        related_name='notifications',
        on_delete=models.CASCADE,
    )
    subject = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    massage = models.TextField()
    status = models.CharField(
        max_length=10,
        choices=StatusChoices,
    )
    group_notification = models.CharField(
        max_length=10,
        choices=GroupNotificationChoices,
    )
    exc_info = models.TextField(
        blank=True,
        null=True,
    )
    created = models.DateTimeField(
        auto_now_add=True,
    )
