import logging

from django.db import models
from django.contrib.auth.models import User


db_logger = logging.getLogger('db')


class Notification(models.Model):

    CREATE = 'create'
    SUCCESS = 'success'
    ERROR = 'error'
    StatusChoices = (
        (CREATE, 'Create'),
        (SUCCESS, 'Success'),
        (ERROR, 'Error'),
    )

    AUTH = 'auth'
    REMINDER = 'reminder'
    GroupNotificationChoices = (
        (AUTH, 'Auth'),
        (REMINDER, 'Reminder'),
    )

    user = models.ForeignKey(
        User,
        related_name='notifications',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    recipient_email = models.CharField(
        max_length=255,
    )
    subject = models.CharField(
        max_length=100,
    )
    message = models.TextField()
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

    def send(self):
        from apps.notification.tasks import send_email

        send_email.apply_async(
            kwargs={
                'notification_id': self.id,
                'recipient': self.recipient_email,
            },
            queue='notification',
        )

    def __str__(self):
        return f'Notification [{self.id}]'
