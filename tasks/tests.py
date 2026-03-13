from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from statuses.models import Status
from .models import Task


class TaskCRUDTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.other_user = User.objects.create_user(username='other', password='12345')
        self.status = Status.objects.create(name='Новый')
        self.task = Task.objects.create(
            name='Тестовая задача',
            description='Описание',
            status=self.status,
            author=self.user,
            executor=self.other_user
        )

    def test_list_tasks_not_logged_in(self):
        response = self.client.get(reverse('tasks'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('tasks')}")

    def test_list_tasks_logged_in(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('tasks'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Тестовая задача')

    def test_create_task_not_logged_in(self):
        response = self.client.get(reverse('task_create'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('task_create')}")

    def test_create_task_logged_in(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('task_create'), {
            'name': 'Новая задача',
            'description': 'Описание новой',
            'status': self.status.id,
            'executor': self.other_user.id,
        })
        self.assertRedirects(response, reverse('tasks'))
        self.assertTrue(Task.objects.filter(name='Новая задача').exists())
        task = Task.objects.get(name='Новая задача')
        self.assertEqual(task.author, self.user)

    def test_update_task(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('task_update', args=[self.task.id]), {
            'name': 'Изменённая задача',
            'description': 'Новое описание',
            'status': self.status.id,
            'executor': '',
        })
        self.assertRedirects(response, reverse('tasks'))
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, 'Изменённая задача')
        self.assertIsNone(self.task.executor)

    def test_delete_task_by_author(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('task_delete', args=[self.task.id]))
        self.assertRedirects(response, reverse('tasks'))
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())

    def test_delete_task_by_non_author(self):
        self.client.login(username='other', password='12345')
        response = self.client.post(reverse('task_delete', args=[self.task.id]))
        self.assertRedirects(response, reverse('tasks'))
        self.assertTrue(Task.objects.filter(id=self.task.id).exists())
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]), 'Задачу может удалить только ее автор'
            )

    def test_unique_name_validation(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('task_create'), {
            'name': 'Тестовая задача',
            'status': self.status.id,
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'уже существует')