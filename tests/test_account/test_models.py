from django.test import TestCase
from django.contrib.auth.models import User

from apps.account.models import Profile
from apps.workout.models import Category, Workout
from apps.history.models import WorkoutHistory


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

    def test_write_history_workout_change_none_program(self):
        user = User.objects.create_user('test_user_1')
        category = Category.objects.create(title='tets_category')
        workout = Workout.objects.create(
            title='test_workout',
            category=category,
            user=user,
        )

        self.assertEqual(WorkoutHistory.objects.count(), 0)
        user.profile.workout = workout
        user.save()

        self.assertEqual(WorkoutHistory.objects.count(), 1)
        history = WorkoutHistory.objects.first()
        self.assertIsNone(history.close_date)

    def test_write_history_workout_change_program_program(self):
        user = User.objects.create_user('test_user_1')
        category = Category.objects.create(title='tets_category')
        workout = Workout.objects.create(
            title='test_workout',
            category=category,
            user=user,
        )
        workout_other = Workout.objects.create(
            title='test_workout_other',
            category=category,
            user=user,
        )
        user.profile.workout = workout
        user.save()

        self.assertEqual(WorkoutHistory.objects.count(), 1)
        history = WorkoutHistory.objects.first()
        self.assertIsNone(history.close_date)

        user.profile.workout = workout_other
        user.save()

        history.refresh_from_db()
        self.assertTrue(history.close_date)

        history_new = WorkoutHistory.objects.filter(
            user=user,
            workout=workout_other,
            close_date__isnull=True,
        ).first()
        self.assertIsNone(history_new.close_date)
        self.assertEqual(WorkoutHistory.objects.count(), 2)

    def test_write_history_workout_change_program_none(self):
        user = User.objects.create_user('test_user_1')
        category = Category.objects.create(title='tets_category')
        workout = Workout.objects.create(
            title='test_workout',
            category=category,
            user=user,
        )
        user.profile.workout = workout
        user.save()

        self.assertEqual(WorkoutHistory.objects.count(), 1)
        history = WorkoutHistory.objects.first()
        self.assertIsNone(history.close_date)

        user.profile.workout = None
        user.save()

        history.refresh_from_db()
        self.assertTrue(history.close_date)
        self.assertEqual(WorkoutHistory.objects.count(), 1)
