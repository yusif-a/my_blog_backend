from django.test import TestCase
from django.urls import reverse
from .views import PostViewSet
from individuals.models import User


class PostViewSetTests(TestCase):
    superuser_data = {'username': 'admin', 'password': 'password'}
    user_data = {'username': 'user', 'password': 'password'}
    superuser = None
    user = None

    @classmethod
    def setUpTestData(cls):
        cls.superuser = User(is_superuser=True, **cls.superuser_data)
        cls.superuser.set_password(cls.superuser_data['password'])
        cls.superuser.save()

        cls.user = User(**cls.user_data)
        cls.user.set_password(cls.user_data['password'])
        cls.user.save()

    def test_superuser_can_create(self):
        self.client.login(**self.superuser_data)
        response = self.client.post(reverse('contents:post-list'), data={'title': 'title', 'text': 'text'})
        self.assertEqual(response.status_code, 201)

    def test_normal_user_cant_create(self):
        self.client.login(**self.user_data)
        response = self.client.post(reverse('contents:post-list'), data={'title': 'title', 'text': 'text'})
        self.assertIn(response.status_code, [401, 403])

    def test_unauthenticated_user_cant_create(self):
        response = self.client.post(reverse('contents:post-list'), data={'title': 'title', 'text': 'text'})
        self.assertIn(response.status_code, [401, 403])

