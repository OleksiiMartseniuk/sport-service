from unittest.mock import patch, MagicMock

from django.test import TestCase

from apps.notification.models import Notification
from apps.notification.tasks import send_email


class TestTasks(TestCase):

    @patch('apps.notification.tasks.send_mail')
    def test_send_email(self, send_mail_mock: MagicMock):
        notification = Notification.objects.create(
            subject='subject',
            message='message',
            status=Notification.CREATE,
            group_notification=Notification.AUTH,
        )
        send_email(
            notification_id=notification.id,
            recipient='test@mail.com',
        )

        send_mail_mock.assert_called()
        notification_update = Notification.objects.get(id=notification.id)
        self.assertEqual(notification_update.status, Notification.SUCCESS)

    @patch('apps.notification.tasks.send_mail')
    def test_send_email_rase_error(self, send_mail_mock: MagicMock):
        send_mail_mock.side_effect = ValueError()

        notification = Notification.objects.create(
            subject='subject',
            message='message',
            status=Notification.CREATE,
            group_notification=Notification.AUTH,
        )
        send_email(
            notification_id=notification.id,
            recipient='test@mail.com',
        )

        send_mail_mock.assert_called()
        notification_update = Notification.objects.get(id=notification.id)
        self.assertEqual(notification_update.status, Notification.ERROR)
