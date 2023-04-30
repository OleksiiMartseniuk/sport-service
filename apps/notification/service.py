from .models import Notification


def create_notification(
    user_id: int | None,
    message: str,
    group_notification: str,
    subject: str | None = None,
) -> Notification:
    return Notification.objects.create(
        user_id=user_id,
        subject=subject,
        message=message,
        status=Notification.CREATE,
        group_notification=group_notification,
    )
