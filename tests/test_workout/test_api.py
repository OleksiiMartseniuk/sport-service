import io

from unittest.mock import MagicMock, patch
from PIL import Image

from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient

from django.contrib.auth.models import User
from django.core.files import File

from apps.workout.models import Category, Workout, Exercise
from apps.notification.models import Notification
from apps.history.models import WorkoutHistory


class TestApi(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create_user('test_user')
        self.client.force_authenticate(self.user)
        self.client.force_authenticate(user=self.user)

    def generate_image_file(self):
        file = io.BytesIO()
        image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(file, 'png')
        file.seek(0)
        return File(file, name='test.png')

    def test_category(self):
        Category.objects.bulk_create(
            [
                Category(title='one'),
                Category(title='two'),
                Category(title='three'),
            ],
        )
        url = reverse('categories')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        result = response.json()['results']
        categories = Category.objects.all().order_by('title')

        self.assertIsInstance(result, list)
        for category_db, category_res in zip(categories, result):
            self.assertEqual(category_db.id, category_res['id'])
            self.assertEqual(category_db.title, category_res['title'])

    def test_workout_create(self):
        category = Category.objects.create(title='tets_category')

        self.assertEqual(Workout.objects.count(), 0)

        url = reverse('workout-list')
        response = self.client.post(
            url,
            data={
                'title': 'test_workout',
                'category': category.id,
            },
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Workout.objects.count(), 1)

        workout_res = response.json()
        workout = Workout.objects.all().first()

        self.assertEqual(workout.id, workout_res['id'])
        self.assertEqual(workout.title, workout_res['title'])
        self.assertEqual(workout.category.id, workout_res['category'])

    def test_workout_list(self):
        category = Category.objects.create(title='tets_category')
        workouts = Workout.objects.bulk_create(
            [
                Workout(title='test_workout', category=category),
                Workout(title='test_workout1', category=category),
                Workout(title='test_workout2', category=category),
            ],
        )

        url = reverse('workout-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        workouts_res = response.json()['results']

        for workout, workout_res in zip(workouts, workouts_res):
            self.assertEqual(workout.id, workout_res['id'])
            self.assertEqual(workout.title, workout_res['title'])
            self.assertEqual(workout.category.id, workout_res['category'])

    def test_workout_retrieve(self):
        category = Category.objects.create(title='tets_category')
        workout = Workout.objects.create(
            title='test_workout',
            category=category,
        )

        url = reverse('workout-detail', kwargs={'pk': workout.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        workout_res = response.json()
        self.assertEqual(workout.id, workout_res['id'])
        self.assertEqual(workout.user, None)
        self.assertEqual(workout.category.id, workout_res['category']['id'])

    def test_workout_update(self):
        category = Category.objects.create(title='tets_category')
        workout = Workout.objects.create(
            title='test_workout',
            category=category,
            user=self.user,
        )

        new_title = 'update_title'
        url = reverse('workout-detail', kwargs={'pk': workout.id})
        response = self.client.put(url, data={'title': new_title})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['title'], new_title)

        workout_update = Workout.objects.first()
        self.assertEqual(workout_update.title, new_title)

    def test_workout_update_not_permission(self):
        category = Category.objects.create(title='tets_category')
        workout = Workout.objects.create(
            title='test_workout',
            category=category,
        )

        new_title = 'update_title'
        url = reverse('workout-detail', kwargs={'pk': workout.id})
        response = self.client.put(url, data={'title': new_title})
        self.assertEqual(response.status_code, 403)

    @patch('apps.notification.models.Notification.send')
    def test_workout_destroy(self, send_mock: MagicMock):
        category = Category.objects.create(title='tets_category')
        workout = Workout.objects.create(
            title='test_workout',
            category=category,
            user=self.user,
        )
        user_test = User.objects.create_user('test_user_2')
        user_test.profile.workout = workout
        user_test.save()
        Exercise.objects.create(
            title='exercise_test',
            workout=workout,
            number_approaches=1,
            number_repetitions=1,
            rest_second=1,
            day=Exercise.MONDAY,
            image=self.generate_image_file(),
        )
        self.assertEqual(Notification.objects.count(), 0)

        url = reverse('workout-detail', kwargs={'pk': workout.id})
        response = self.client.delete(url)

        send_mock.assert_called()
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Workout.objects.count(), 0)
        self.assertEqual(Exercise.objects.count(), 0)
        user_test = User.objects.get(username='test_user_2')
        self.assertIsNone(user_test.profile.workout)
        self.assertEqual(Notification.objects.count(), 1)
        history = WorkoutHistory.objects.first()
        self.assertTrue(history.data_close)
        self.assertEqual(
            history.detail_info[1]['event'],
            f'Owner {workout.user.username} workout removed workout',
        )

    def test_exercise_create(self):
        category = Category.objects.create(title='tets_category')
        workout = Workout.objects.create(
            title='test_workout',
            category=category,
            user=self.user,
        )
        url = reverse('exercise-list')

        exercise_data = {
            'title': 'exercise_test',
            'number_approaches': 1,
            'number_repetitions': 1,
            'rest_second': 1,
            'day': Exercise.MONDAY,
            'workout': workout.id,
            'image': self.generate_image_file(),
        }
        response = self.client.post(
            url,
            data=exercise_data,
            format='multipart',
        )
        self.assertEqual(response.status_code, 201)

        exercise_res = response.json()
        self.assertEqual(exercise_res['title'], exercise_data['title'])
        self.assertEqual(exercise_res['day'], exercise_data['day'])
        self.assertEqual(exercise_res['workout'], exercise_data['workout'])
        self.assertEqual(
            exercise_res['number_approaches'],
            exercise_data['number_approaches'],
        )
        self.assertEqual(
            exercise_res['number_repetitions'],
            exercise_data['number_repetitions'],
        )
        self.assertEqual(
            exercise_res['rest_second'],
            exercise_data['rest_second'],
        )
        Exercise.objects.first().image.delete()

    def test_exercise_create_not_permission(self):
        user = User.objects.create_user('test_user_1')
        category = Category.objects.create(title='tets_category')
        workout = Workout.objects.create(
            title='test_workout',
            category=category,
            user=user,
        )
        url = reverse('exercise-list')

        exercise_data = {
            'title': 'exercise_test',
            'number_approaches': 1,
            'number_repetitions': 1,
            'rest_second': 1,
            'day': Exercise.MONDAY,
            'workout': workout.id,
            'image': self.generate_image_file(),
        }
        response = self.client.post(
            url,
            data=exercise_data,
            format='multipart',
        )
        self.assertEqual(response.status_code, 403)

    def test_exercise_retrieve(self):
        category = Category.objects.create(title='tets_category')
        workout = Workout.objects.create(
            title='test_workout',
            category=category,
            user=self.user,
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

        url = reverse('exercise-detail', kwargs={'pk': exercise.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        exercise_res = response.json()

        self.assertEqual(exercise.id, exercise_res['id'])
        self.assertEqual(exercise.workout.id, exercise_res['workout']['id'])
        self.assertEqual(
            exercise.workout.category.id,
            exercise_res['workout']['category']['id'],
        )
        self.assertEqual(
            exercise.workout.user.id,
            exercise_res['workout']['user']['id'],
        )
        Exercise.objects.first().image.delete()

    def test_exercise_update(self):
        category = Category.objects.create(title='tets_category')
        workout = Workout.objects.create(
            title='test_workout',
            category=category,
            user=self.user,
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

        url = reverse('exercise-detail', kwargs={'pk': exercise.id})
        response = self.client.put(url, data={'title': 'update_title'})

        self.assertEqual(response.status_code, 200)

        exercise_res = response.json()
        exercise_update = Exercise.objects.first()
        self.assertEqual(exercise_update.title, exercise_res['title'])
        Exercise.objects.first().image.delete()

    def test_exercise_update_not_permission(self):
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
        url = reverse('exercise-detail', kwargs={'pk': exercise.id})
        response = self.client.put(url, data={'title': 'update_title'})
        self.assertEqual(response.status_code, 403)
        Exercise.objects.first().image.delete()

    def test_exercise_delete(self):
        category = Category.objects.create(title='tets_category')
        workout = Workout.objects.create(
            title='test_workout',
            category=category,
            user=self.user,
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
        url = reverse('exercise-detail', kwargs={'pk': exercise.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertIsNone(Exercise.objects.first())

    def test_exercise_delete_not_permission(self):
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
        url = reverse('exercise-detail', kwargs={'pk': exercise.id})

        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Exercise.objects.count(), 1)
        Exercise.objects.first().image.delete()
