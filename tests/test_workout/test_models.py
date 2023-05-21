from unittest.mock import MagicMock, patch

from django.test import TestCase
from django.contrib.auth.models import User

from apps.workout.models import Category, Workout


class TestModels(TestCase):

    @patch('apps.notification.models.Notification.send')
    def test_change_publish(self, send_mock: MagicMock):
        user = User.objects.create_user('user_test')
        category = Category.objects.create(title='tets_category')
        workout = Workout.objects.create(
            title='test_workout',
            category=category,
        )
        user.profile.workout = workout
        user.save()

        self.assertEqual(user.profile.workout, workout)

        workout.publish = False
        workout.save()

        send_mock.assert_called()

        user = User.objects.first()
        self.assertIsNone(user.profile.workout)
