import io

from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.files import File

from PIL import Image

from apps.workout.models import Category, Workout, Exercise
from apps.history.models import WorkoutHistory, ExerciseHistory
from apps.history.service import WorkoutHistoryAction, ExerciseHistoryAction


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
