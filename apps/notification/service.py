import os

from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.conf import settings

from .models import Notification


def create_notification(
    recipient_email: str,
    message: str,
    subject: str,
    group_notification: str,
    user_id: int | None = None,
    html_message: str | None = None,
) -> Notification:
    return Notification.objects.create(
        user_id=user_id,
        recipient_email=recipient_email,
        subject=subject,
        message=message,
        html_message=html_message,
        status=Notification.CREATE,
        group_notification=group_notification,
    )


def send_notification_at_remove_workout(
    users_id: list,
    workout_title: str,
) -> None:
    users = User.objects.filter(id__in=users_id)

    for user in users:
        html_message = render_to_string(
            template_name=os.path.join(
                settings.TEMPLATE_NOTIFICATION,
                'remove_workout.html',
            ),
            context={
                'username': user.username,
                'program_name': workout_title,
            },
        )
        notification = create_notification(
            recipient_email=user.email,
            message=html_message,
            subject='Removed workout',
            group_notification=Notification.ACTION,
            user_id=user.id,
            html_message=html_message,
        )
        notification.send()
