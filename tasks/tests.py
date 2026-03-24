from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from labels.models import Label
from statuses.models import Status
from tasks.models import Task


class TaskCRUDTest(TestCase):
    fixtures = ['users', 'statuses', 'labels']

    def setUp(self):
        self.user = User.objects.get(username='testuser')
        self.other_user = User.objects.get(username='other')
        self.status = Status.objects.get(pk=1)
        self.label = Label.objects.get(pk=1)

    def test_list_tasks_not_logged_in(self):
        response = self.client.get(reverse('tasks:list'))
        self.assertRedirects(
            response, f"{reverse('login')}?next={reverse('tasks:list')}"
        )

    def test_list_tasks_logged_in(self):
        self.client.login(username='testuser', password='12345')
        Task.objects.create(
            name='Тестовая задача', status=self.status, author=self.user
        )
        response = self.client.get(reverse('tasks:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Тестовая задача')

    def test_create_task_not_logged_in(self):
        response = self.client.get(reverse('tasks:create'))
        self.assertRedirects(
            response, f"{reverse('login')}?next={reverse('tasks:create')}"
        )

    def test_create_task_logged_in(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('tasks:create'), {
            'name': 'Новая задача',
            'description': 'Описание новой',
            'status': self.status.id,
            'executor': self.other_user.id,
            'labels': [self.label.id],
        }, follow=True)
        self.assertRedirects(response, reverse('tasks:list'))
        self.assertTrue(Task.objects.filter(name='Новая задача').exists())
        new_task = Task.objects.get(name='Новая задача')
        self.assertEqual(new_task.author, self.user)
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Задача успешно создана')

    def test_update_task(self):
        self.client.login(username='testuser', password='12345')
        task = Task.objects.create(
            name='Задача для обновления',
            status=self.status,
            author=self.user,
        )
        response = self.client.post(reverse('tasks:update', args=[task.id]), {
            'name': 'Изменённая задача',
            'status': self.status.id,
            'executor': '',
        }, follow=True)
        self.assertRedirects(response, reverse('tasks:list'))
        task.refresh_from_db()
        self.assertEqual(task.name, 'Изменённая задача')

    def test_delete_task_by_author(self):
        self.client.login(username='testuser', password='12345')
        task = Task.objects.create(
            name='Задача на удаление',
            status=self.status,
            author=self.user,
        )
        response = self.client.post(
            reverse('tasks:delete', args=[task.id]), follow=True
        )
        self.assertRedirects(response, reverse('tasks:list'))
        self.assertFalse(Task.objects.filter(id=task.id).exists())

    def test_delete_task_by_non_author(self):
        self.client.login(username='testuser', password='12345')
        task = Task.objects.create(
            name='Чужая задача',
            status=self.status,
            author=self.other_user,
        )
        response = self.client.post(
            reverse('tasks:delete', args=[task.id]), follow=True
        )
        self.assertRedirects(response, reverse('tasks:list'))
        self.assertTrue(Task.objects.filter(id=task.id).exists())
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(
            str(messages[0]), 'Задачу может удалить только ее автор'
        )

    def test_unique_name_validation(self):
        self.client.login(username='testuser', password='12345')
        Task.objects.create(
            name='Уникальное имя', status=self.status, author=self.user
        )
        response = self.client.post(reverse('tasks:create'), {
            'name': 'Уникальное имя',
            'status': self.status.id,
        })
        self.assertEqual(response.status_code, 200)
        content = response.content.decode()
        self.assertTrue(
            'already exists' in content or 'уже существует' in content
        )

    def test_delete_task_with_labels(self):
        self.client.login(username='testuser', password='12345')
        task = Task.objects.create(
            name='Задача с метками',
            status=self.status,
            author=self.user,
        )
        task.labels.add(self.label)
        response = self.client.post(
            reverse('tasks:delete', args=[task.id]), follow=True
        )
        self.assertRedirects(response, reverse('tasks:list'))
        self.assertFalse(Task.objects.filter(id=task.id).exists())
        self.assertTrue(Label.objects.filter(id=self.label.id).exists())