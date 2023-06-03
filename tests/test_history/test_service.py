from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone

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
        )
        self.assertEqual(WorkoutHistory.objects.count(), 1)

        history: WorkoutHistory = WorkoutHistory.objects.first()

        self.assertEqual(history.workout, workout)
        self.assertEqual(history.user, user)
        self.assertEqual(
            history.detail_info[0]['event'],
            f'The program #{workout.title} was started',
        )

    def test_current_workout_history(self):
        user = User.objects.create_user('user_test')
        category = Category.objects.create(title='tets_category')
        workout = Workout.objects.create(
            title='test_workout',
            category=category,
        )
        # close workout
        WorkoutHistory.objects.create(
            user=user,
            workout=workout,
            data_close=timezone.now(),
        )
        # current workout
        history = WorkoutHistory.objects.create(
            user=user,
            workout=workout,
        )
        current_history = HistoryAction.get_current_workout_history(
            user=user,
            workout=workout,
        )
        self.assertEqual(history, current_history)
