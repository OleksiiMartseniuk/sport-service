from django.contrib.auth.models import User

from .models import Notification


def create_notification(
    user: User,
    massage: str,
    group_notification: str,
    subject: str | None = None,
) -> Notification:
    return Notification.objects.create(
        user=user,
        subject=subject,
        massage=massage,
        status=Notification.CREATE,
        group_notification=group_notification,
    )
