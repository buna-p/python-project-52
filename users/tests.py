from django.test import TestCase

from django.contrib.auth.models import User
from django.urls import reverse


class UserCRUDTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='12345'
            )
        self.other_user = User.objects.create_user(
            username='other', password='12345'
            )

    def test_user_list_view(self):
        response = self.client.get(reverse('users'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testuser')
        self.assertContains(response, 'other')

    def test_registration(self):
        response = self.client.post(reverse('user_create'), {
            'username': 'newuser',
            'password1': 'complex_password_123',
            'password2': 'complex_password_123',
        })
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(username='newuser').exists())
        response = self.client.get(reverse('login'))
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]), 'Пользователь успешно зарегистрирован'
            )

    def test_login(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': '12345',
        })
        self.assertRedirects(response, reverse('index'))
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_logout(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('logout'))
        self.assertRedirects(response, reverse('index'))
        self.assertFalse('_auth_user_id' in self.client.session)

    def test_user_update(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse(
            'user_update', args=[self.user.id]), {
            'username': 'updateduser',
            'first_name': 'Updated',
            'last_name': 'User',
        })
        self.assertRedirects(response, reverse('users'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateduser')
        self.assertEqual(self.user.first_name, 'Updated')
        response = self.client.post(reverse(
            'user_update', args=[self.other_user.id]), {
            'username': 'unknown',
        })
        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(username='unknown').exists())

    def test_user_delete(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('user_delete', args=[self.user.id]))
        self.assertRedirects(response, reverse('users'))
        self.assertFalse(User.objects.filter(id=self.user.id).exists())
        response = self.client.post(reverse(
            'user_delete', args=[self.other_user.id]
            ))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(id=self.other_user.id).exists())