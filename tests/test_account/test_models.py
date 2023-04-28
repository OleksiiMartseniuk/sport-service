from django.test import TestCase
from django.contrib.auth.models import User

from apps.account.models import Profile


class TestModels(TestCase):

    def test_create_user(self):
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(Profile.objects.count(), 0)

        User.objects.create_user(
            username='test',
            email='test@mail.com',
            password='test',
        )

        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Profile.objects.count(), 1)

    def test_update_profile(self):
        self.assertEqual(User.objects.count(), 0)
        self.assertEqual(Profile.objects.count(), 0)

        user = User.objects.create_user(
            username='test',
            email='test@mail.com',
            password='test',
        )

        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(Profile.objects.count(), 1)

        profile = Profile.objects.get(owner=user)

        self.assertEqual(profile.reminder_time, None)

        user.profile.reminder_time = Profile.DAY
        user.save()

        profile = Profile.objects.get(owner=user)
        self.assertEqual(profile.reminder_time, Profile.DAY)
