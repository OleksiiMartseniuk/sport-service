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


class SendNotification:

    def __init__(self) -> None:
        self.template_path = settings.TEMPLATE_NOTIFICATION

    def __send_notification_users(
        self,
        users_id: list,
        template_context: dict,
        template_name: str,
        group_notification: str,
        subject: str,
    ) -> None:
        users = User.objects.filter(id__in=users_id)

        for user in users:
            html_message = render_to_string(
                template_name=os.path.join(self.template_path, template_name),
                context={'user': user, **template_context},
            )
            notification = create_notification(
                recipient_email=user.email,
                message=html_message,
                subject=subject,
                group_notification=group_notification,
                user_id=user.id,
                html_message=html_message,
            )
            notification.send()

    def send_notification_at_publish(
        self,
        users_id: list,
        workout_title: str,
    ) -> None:
        self.__send_notification_users(
            users_id=users_id,
            template_name='publish_workout.html',
            template_context={'program_name': workout_title},
            group_notification=Notification.SYSTEM,
            subject='Workout blocked',
        )

    def send_notification_at_remove_workout(
        self,
        users_id: list,
        workout_title: str,
    ) -> None:
        self.__send_notification_users(
            users_id=users_id,
            template_name='remove_workout.html',
            template_context={'program_name': workout_title},
            group_notification=Notification.ACTION,
            subject='Removed workout',
        )
