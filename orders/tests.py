from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AuthFlowTests(TestCase):
    def test_register_view_creates_user(self):
        response = self.client.post(
            reverse('register'),
            {
                'username': 'newuser',
                'first_name': 'New',
                'last_name': 'User',
                'email': 'newuser@example.com',
                'password1': 'StrongPass123',
                'password2': 'StrongPass123',
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        user = get_user_model().objects.get(username='newuser')
        self.assertEqual(user.first_name, 'New')
        self.assertEqual(user.last_name, 'User')
        self.assertEqual(user.email, 'newuser@example.com')
        self.assertContains(response, 'Hi, newuser')

    def test_login_view_authenticates_existing_user(self):
        user = get_user_model().objects.create_user(
            username='existinguser',
            password='StrongPass123',
        )

        response = self.client.post(
            reverse('login'),
            {
                'username': 'existinguser',
                'password': 'StrongPass123',
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f'Hi, {user.username}')
        self.assertTrue(response.wsgi_request.user.is_authenticated)
