from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Status


class StatusCRUDTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='12345'
            )
        self.status = Status.objects.create(name='Новый')

    def test_list_statuses_not_logged_in(self):
        response = self.client.get(reverse('statuses'))
        self.assertRedirects(
            response, f"{reverse('login')}?next={reverse('statuses')}"
            )

    def test_list_statuses_logged_in(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('statuses'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Новый')

    def test_create_status_not_logged_in(self):
        response = self.client.get(reverse('status_create'))
        self.assertRedirects(
            response, f"{reverse('login')}?next={reverse('status_create')}"
            )

    def test_create_status_logged_in(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(
            reverse('status_create'), {'name': 'В работе'}, follow=True
            )
        self.assertRedirects(response, reverse('statuses'))
        self.assertTrue(Status.objects.filter(name='В работе').exists())
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Статус успешно создан')

    def test_update_status(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(
            reverse('status_update', args=[self.status.id]), {'name': 'Изменён'}
            )
        self.assertRedirects(response, reverse('statuses'))
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, 'Изменён')

    def test_delete_status(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse(
            'status_delete', args=[self.status.id]))
        self.assertRedirects(response, reverse('statuses'))
        self.assertFalse(Status.objects.filter(id=self.status.id).exists())

    def test_unique_name_validation(self):
        self.client.login(username='testuser', password='12345')
        Status.objects.create(name='Уникальный')
        response = self.client.post(
            reverse('status_create'), {'name': 'Уникальный'}
            )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'уже существует')
