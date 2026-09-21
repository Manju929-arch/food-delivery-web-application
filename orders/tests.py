from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse


class AuthFlowTests(TestCase):
    def test_register_view_creates_user(self):
        response = self.client.post(
            reverse('register'),
            {
                'username': 'newuser',
                'password1': 'StrongPass123',
                'password2': 'StrongPass123',
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertTrue(get_user_model().objects.filter(username='newuser').exists())
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
