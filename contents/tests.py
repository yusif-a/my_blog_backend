from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from .views import PostViewSet
from .models import Post
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

        cls.writers_group = Group.objects.create(name='writers')
        post_content_type = ContentType.objects.get_for_model(Post)
        permissions = Permission.objects.filter(
            content_type=post_content_type,
            codename__in=['add_post', 'change_post', 'delete_post', 'view_post'])
        cls.writers_group.permissions.add(*permissions)

    def test_superuser_can_create(self):
        self.client.login(**self.superuser_data)
        response = self.client.post(reverse('contents:post-list'), data={'title': 'title', 'text': 'text'})
        self.assertEqual(response.status_code, 201)

    def test_normal_user_cant_create(self):
        self.client.login(**self.user_data)
        response = self.client.post(reverse('contents:post-list'), data={'title': 'title', 'text': 'text'})
        self.assertIn(response.status_code, [401, 403])

    def test_normal_user_with_granted_perms_can_create(self):
        self.user.groups.add(self.writers_group)
        self.client.login(**self.user_data)
        response = self.client.post(reverse('contents:post-list'), data={'title': 'title', 'text': 'text'})
        self.assertEqual(response.status_code, 201)

    def test_unauthenticated_user_cant_create(self):
        response = self.client.post(reverse('contents:post-list'), data={'title': 'title', 'text': 'text'})
        self.assertIn(response.status_code, [401, 403])

