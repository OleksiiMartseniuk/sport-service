import io

from unittest import mock

from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.files import File

from PIL import Image

from apps.workout.models import Category, Workout, Exercise
from apps.history.models import (
    WorkoutHistory,
    ExerciseHistory,
    ExerciseApproach,
)
from apps.history.service import WorkoutHistoryAction, ExerciseHistoryAction
from apps.history.exceptions import WorkoutHistoryNotFound


class TestService(TestCase):

    def generate_image_file(self):
        file = io.BytesIO()
        image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(file, 'png')
        file.seek(0)
        return File(file, name='test.png')

    def test_create_workout_history(self):
        self.assertEqual(WorkoutHistory.objects.count(), 0)
        user = User.objects.create_user('user_test')
        category = Category.objects.create(title='tets_category')
        workout = Workout.objects.create(
            title='test_workout',
            category=category,
        )
        WorkoutHistoryAction.create_workout(
            user=user,
            workout=workout,
        )
        self.assertEqual(WorkoutHistory.objects.count(), 1)

        history: WorkoutHistory = WorkoutHistory.objects.first()

        self.assertEqual(history.workout, workout)
        self.assertEqual(history.user, user)
        self.assertEqual(
            history.event.first().title,
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
            close_date=timezone.now(),
        )
        # current workout
        history = WorkoutHistory.objects.create(
            user=user,
            workout=workout,
        )
        current_history = WorkoutHistoryAction.get_current_workout_history(
            user=user,
            workout=workout,
        )
        self.assertEqual(history, current_history)

    def test_get_or_create_exercise_history_new(self):
        user = User.objects.create_user('user_test')
        category = Category.objects.create(title='tets_category')
        workout = Workout.objects.create(
            title='test_workout',
            category=category,
        )
        exercise = Exercise.objects.create(
            title='exercise_test',
            workout=workout,
            number_approaches=1,
            number_repetitions=1,
            rest_second=1,
            day=Exercise.MONDAY,
            image=self.generate_image_file(),
        )

        user.profile.workout = workout
        user.save()

        self.assertEqual(ExerciseHistory.objects.count(), 0)
        exercise_history = ExerciseHistoryAction().get_or_create(
            user=user,
            workout=workout,
            exercise=exercise,
        )

        self.assertEqual(exercise_history.exercises, exercise)
        self.assertEqual(exercise_history.workout_title, workout.title)
        self.assertEqual(ExerciseHistory.objects.count(), 1)
        Exercise.objects.first().image.delete()

    def test_get_or_create_exercise_history_get(self):
        user = User.objects.create_user('user_test')
        category = Category.objects.create(title='tets_category')
        workout = Workout.objects.create(
            title='test_workout',
            category=category,
        )
        exercise = Exercise.objects.create(
            title='exercise_test',
            workout=workout,
            number_approaches=1,
            number_repetitions=1,
            rest_second=1,
            day=Exercise.MONDAY,
            image=self.generate_image_file(),
        )

        user.profile.workout = workout
        user.save()

        exercise_history_new = ExerciseHistory.objects.create(
            exercises_title=exercise.title,
            workout_title=workout.title,
            exercises=exercise,
            history_workout=user.history_workout.first(),
            close_date=None,
        )

        exercise_history_current = ExerciseHistoryAction().get_or_create(
            user=user,
            workout=workout,
            exercise=exercise,
        )

        self.assertEqual(exercise_history_new, exercise_history_current)

    @mock.patch('apps.history.service.ExerciseHistoryAction.get_or_create')
    def test_add_exercise_approach(self, get_or_create_mock: mock.MagicMock):
        user = User.objects.create_user('user_test')
        category = Category.objects.create(title='tets_category')
        workout = Workout.objects.create(
            title='test_workout',
            category=category,
        )
        exercise = Exercise.objects.create(
            title='exercise_test',
            workout=workout,
            number_approaches=2,
            number_repetitions=1,
            rest_second=1,
            day=Exercise.MONDAY,
            image=self.generate_image_file(),
        )

        user.profile.workout = workout
        user.save()

        exercise_history = ExerciseHistory.objects.create(
            exercises_title=exercise.title,
            workout_title=workout.title,
            exercises=exercise,
            history_workout=user.history_workout.first(),
            close_date=None,
        )
        get_or_create_mock.return_value = exercise_history

        self.assertEqual(ExerciseApproach.objects.count(), 0)
        ExerciseHistoryAction().add_exercise_approach(
            workout=workout,
            user=user,
            exercise=exercise,
            number_repetitions=1,
        )
        get_or_create_mock.assert_called_once()
        self.assertEqual(ExerciseApproach.objects.count(), 1)
        exercise_approach = ExerciseApproach.objects.first()

        self.assertEqual(exercise_approach.exercise_history, exercise_history)
        self.assertEqual(exercise_approach.current_approach, 1)
        self.assertEqual(exercise_approach.number_repetitions, 1)
        user.refresh_from_db()
        self.assertIsNone(user.history_workout.first().close_date)
        exercise_history.refresh_from_db()
        self.assertIsNone(exercise_history.close_date)

    @mock.patch('apps.history.service.ExerciseHistoryAction.get_or_create')
    def test_add_exercise_approach_close_exercise_history(
        self,
        get_or_create_mock: mock.MagicMock,
    ):
        user = User.objects.create_user('user_test')
        category = Category.objects.create(title='tets_category')
        workout = Workout.objects.create(
            title='test_workout',
            category=category,
        )
        exercise = Exercise.objects.create(
            title='exercise_test',
            workout=workout,
            number_approaches=1,
            number_repetitions=1,
            rest_second=1,
            day=Exercise.MONDAY,
            image=self.generate_image_file(),
        )

        user.profile.workout = workout
        user.save()

        exercise_history = ExerciseHistory.objects.create(
            exercises_title=exercise.title,
            workout_title=workout.title,
            exercises=exercise,
            history_workout=user.history_workout.first(),
            close_date=None,
        )
        get_or_create_mock.return_value = exercise_history

        self.assertEqual(ExerciseApproach.objects.count(), 0)
        ExerciseHistoryAction().add_exercise_approach(
            workout=workout,
            user=user,
            exercise=exercise,
            number_repetitions=1,
        )
        get_or_create_mock.assert_called_once()
        self.assertEqual(ExerciseApproach.objects.count(), 1)
        exercise_history.refresh_from_db()
        self.assertTrue(exercise_history.close_date)

    def test_close_exercise_history(self):
        user = User.objects.create_user('user_test')
        category = Category.objects.create(title='tets_category')
        workout = Workout.objects.create(
            title='test_workout',
            category=category,
        )
        exercise = Exercise.objects.create(
            title='exercise_test',
            workout=workout,
            number_approaches=1,
            number_repetitions=1,
            rest_second=1,
            day=Exercise.MONDAY,
            image=self.generate_image_file(),
        )

        user.profile.workout = workout
        user.save()

        exercise_history = ExerciseHistory.objects.create(
            exercises_title=exercise.title,
            workout_title=workout.title,
            exercises=exercise,
            history_workout=user.history_workout.first(),
            close_date=None,
        )

        self.assertIsNone(exercise_history.close_date)
        ExerciseHistoryAction.close_exercise_history(
            exercise_id=exercise.id,
            user=user,
        )
        exercise_history.refresh_from_db()
        self.assertTrue(exercise_history.close_date)

    def test_close_exercise_history_not_history_workout(self):
        user = User.objects.create_user('user_test')
        self.assertRaises(
            WorkoutHistoryNotFound,
            ExerciseHistoryAction.close_exercise_history,
            1,
            user,
        )

    def test_close_exercise_history_not_exercise_history(self):
        user = User.objects.create_user('user_test')
        category = Category.objects.create(title='tets_category')
        workout = Workout.objects.create(
            title='test_workout',
            category=category,
        )
        user.profile.workout = workout
        user.save()

        self.assertRaises(
            WorkoutHistoryNotFound,
            ExerciseHistoryAction.close_exercise_history,
            1,
            user,
        )
