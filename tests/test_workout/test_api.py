from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient

from django.contrib.auth.models import User

from apps.workout.models import Category


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

        result = response.json()['results']
        categories = Category.objects.all().order_by('title')

        self.assertIsInstance(result, list)
        for category_db, category_res in zip(categories, result):
            self.assertEqual(category_db.id, category_res['id'])
            self.assertEqual(category_db.title, category_res['title'])
