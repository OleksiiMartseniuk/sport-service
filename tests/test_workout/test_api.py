from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient

from django.contrib.auth.models import User

from apps.workout.models import Category, Workout


class TestApi(TestCase):

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = User.objects.create_user('test_user')
        self.client.force_authenticate(self.user)
        self.client.force_authenticate(user=self.user)

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

    def test_workout_destroy(self):
        category = Category.objects.create(title='tets_category')
        workout = Workout.objects.create(
            title='test_workout',
            category=category,
            user=self.user,
        )

        url = reverse('workout-detail', kwargs={'pk': workout.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 204)
