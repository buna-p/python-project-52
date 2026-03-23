from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from tasks.models import Task

from .models import Status


class StatusCRUDTest(TestCase):
    fixtures = ['users', 'statuses']

    def setUp(self):
        self.user = User.objects.get(username='testuser')
        self.status = Status.objects.get(pk=1)

    def test_list_statuses_not_logged_in(self):
        response = self.client.get(reverse('statuses:list'))
        self.assertRedirects(
            response,
            f"{reverse('users:login')}?next={reverse('statuses:list')}"
        )

    def test_list_statuses_logged_in(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('statuses:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Новый')
        self.assertContains(response, 'В работе')

    def test_create_status_not_logged_in(self):
        response = self.client.get(reverse('statuses:create'))
        self.assertRedirects(
            response,
            f"{reverse('users:login')}?next={reverse('statuses:create')}"
        )

    def test_create_status_logged_in(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(
            reverse('statuses:create'), {'name': 'Тестовый статус'}, follow=True
        )
        self.assertRedirects(response, reverse('statuses:list'))
        self.assertTrue(Status.objects.filter(name='Тестовый статус').exists())
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Статус успешно создан')

    def test_update_status(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(
            reverse('statuses:update', args=[self.status.id]),
            {'name': 'Изменён'},
            follow=True
        )
        self.assertRedirects(response, reverse('statuses:list'))
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, 'Изменён')

    def test_delete_status(self):
        self.client.login(username='testuser', password='12345')
        status = Status.objects.create(name='Удаляемый')
        response = self.client.post(
            reverse('statuses:delete', args=[status.id]), follow=True
        )
        self.assertRedirects(response, reverse('statuses:list'))
        self.assertFalse(Status.objects.filter(id=status.id).exists())

    def test_unique_name_validation(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(
            reverse('statuses:create'), {'name': 'Новый'}
            )
        self.assertEqual(response.status_code, 200)
        content = response.content.decode()
        self.assertTrue(
            'already exists' in content or 'уже существует' in content
        )

    def test_delete_status_associated_with_task(self):
        self.client.login(username='testuser', password='12345')
        Task.objects.create(
            name='Задача со статусом',
            status=self.status,
            author=self.user,
        )
        self.assertTrue(Task.objects.filter(status=self.status).exists())
        response = self.client.post(
            reverse('statuses:delete', args=[self.status.id]), follow=True
        )
        self.assertRedirects(response, reverse('statuses:list'))
        self.assertTrue(Status.objects.filter(id=self.status.id).exists())
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Невозможно удалить статус')
