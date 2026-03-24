from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class UserCRUDTest(TestCase):
    fixtures = ['users']

    def setUp(self):
        self.user = User.objects.get(username='testuser')
        self.other_user = User.objects.get(username='other')

    def test_user_list_view(self):
        response = self.client.get(reverse('users:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testuser')
        self.assertContains(response, 'other')

    def test_registration(self):
        response = self.client.post(reverse('users:create'), {
            'username': 'newuser',
            'password1': 'complex_password_123',
            'password2': 'complex_password_123',
        }, follow=True)
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(username='newuser').exists())
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]), 'Пользователь успешно зарегистрирован'
        )

    def test_login(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': '12345',
        }, follow=True)
        self.assertRedirects(response, reverse('index'))
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_logout(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('logout'), follow=True)
        self.assertRedirects(response, reverse('index'))
        self.assertFalse('_auth_user_id' in self.client.session)

    def test_user_update(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(
            reverse('users:update', args=[self.user.id]), {
                'username': 'updateduser',
                'first_name': 'Updated',
                'last_name': 'User',
            }, follow=True)
        self.assertRedirects(response, reverse('users:list'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateduser')
        self.client.login(username='other', password='12345')
        response = self.client.post(
            reverse('users:update', args=[self.user.id]), {
                'username': 'hacker',
            })
        self.assertEqual(response.status_code, 302)
        self.assertFalse(User.objects.filter(username='hacker').exists())

    def test_user_delete(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(
            reverse('users:delete', args=[self.user.id]), follow=True
        )
        self.assertRedirects(response, reverse('users:list'))
        self.assertFalse(User.objects.filter(id=self.user.id).exists())

    def test_user_delete_other(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(
            reverse('users:delete', args=[self.other_user.id]), follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(User.objects.filter(id=self.other_user.id).exists())
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'У вас нет прав для удаления')