from django.test import TestCase
from django.contrib.auth.models import User

from apps.notification.models import Notification
from apps.notification.service import create_notification


class TestService(TestCase):

    def test_create_notification(self):
        self.assertEqual(Notification.objects.count(), 0)

        user = User.objects.create_user(
            username='test',
            email='test@email.com',
            password='password',
        )

        notification = create_notification(
            user_id=user.id,
            message='test massage',
            group_notification=Notification.AUTH,
        )
        self.assertEqual(Notification.objects.count(), 1)
        notification_new: Notification = Notification.objects.first()

        self.assertEqual(notification_new.id, notification.id)
        self.assertEqual(notification_new.user, notification.user)
        self.assertEqual(notification_new.subject, notification.subject)
        self.assertEqual(notification_new.status, notification.status)
        self.assertEqual(
            notification_new.group_notification,
            notification.group_notification,
        )

    def test_create_notification_not_user(self):
        notification = create_notification(
            user_id=None,
            message='test massage',
            group_notification=Notification.AUTH,
        )

        notification_new: Notification = Notification.objects.first()

        self.assertEqual(notification_new.user, notification.user)
        self.assertIsNone(notification_new.user_id)
