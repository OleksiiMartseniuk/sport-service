from .models import Notification


def create_notification(
    user_id: int | None,
    massage: str,
    group_notification: str,
    subject: str | None = None,
) -> Notification:
    return Notification.objects.create(
        user_id=user_id,
        subject=subject,
        massage=massage,
        status=Notification.CREATE,
        group_notification=group_notification,
    )
