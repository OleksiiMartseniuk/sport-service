from django.test import TestCase
from django.contrib.auth.models import User

from apps.workout.models import Category, Workout
from apps.history.models import WorkoutHistory
from apps.history.service import HistoryAction


class TestService(TestCase):

    def test_create_workout_history(self):
        self.assertEqual(WorkoutHistory.objects.count(), 0)
        user = User.objects.create_user('user_test')
        category = Category.objects.create(title='tets_category')
        workout = Workout.objects.create(
            title='test_workout',
            category=category,
        )
        HistoryAction.create_workout(
            user=user,
            workout=workout,
            detail_info='test_massage',
        )
        self.assertEqual(WorkoutHistory.objects.count(), 1)

        history: WorkoutHistory = WorkoutHistory.objects.first()

        self.assertEqual(history.workout, workout)
        self.assertEqual(history.user, user)
        self.assertEqual(
            list(history.detail_info[0].values()),
            ['test_massage'],
        )
