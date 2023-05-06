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
