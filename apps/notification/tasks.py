import logging

from django.core.mail import send_mail

from config.celery import app

from .models import Notification


db_logger = logging.getLogger('db')


@app.task(queue='notification')
def send_email(notification_id: int, recipient: str):
    try:
        notification = Notification.objects.get(id=notification_id)
    except Notification.DoesNotExist:
        db_logger.error(f'Not found notification [{notification_id}]')
        return

    try:
        send_mail(
            subject=notification.subject,
            message=notification.message,
            recipient_list=[recipient],
            html_message=notification.html_message,
            from_email=None,
            fail_silently=True,
        )
        notification.status = Notification.SUCCESS
    except Exception as ex:
        notification.status = Notification.ERROR
        notification.exc_info = str(ex)
    finally:
        notification.save()
