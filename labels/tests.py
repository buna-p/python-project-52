from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from statuses.models import Status
from tasks.models import Task

from .models import Label


class LabelCRUDTest(TestCase):
    fixtures = ['users', 'labels', 'statuses']

    def setUp(self):
        self.user = User.objects.get(username='testuser')
        self.label = Label.objects.get(pk=1)
        self.status = Status.objects.get(pk=1)

    def test_list_labels_not_logged_in(self):
        response = self.client.get(reverse('labels:list'))
        self.assertRedirects(
            response, f"{reverse('users:login')}?next={reverse('labels:list')}"
        )

    def test_list_labels_logged_in(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('labels:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'bug')
        self.assertContains(response, 'feature')

    def test_create_label_not_logged_in(self):
        response = self.client.get(reverse('labels:create'))
        self.assertRedirects(
            response,
            f"{reverse('users:login')}?next={reverse('labels:create')}"
        )

    def test_create_label_logged_in(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(
            reverse('labels:create'), {'name': 'Тестовая метка'}, follow=True
        )
        self.assertRedirects(response, reverse('labels:list'))
        self.assertTrue(Label.objects.filter(name='Тестовая метка').exists())
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Метка успешно создана')

    def test_update_label(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(
            reverse('labels:update', args=[self.label.id]),
            {'name': 'Изменён'},
            follow=True
        )
        self.assertRedirects(response, reverse('labels:list'))
        self.label.refresh_from_db()
        self.assertEqual(self.label.name, 'Изменён')

    def test_delete_label(self):
        self.client.login(username='testuser', password='12345')
        label = Label.objects.create(name='Удаляемая')
        response = self.client.post(
            reverse('labels:delete', args=[label.id]), follow=True
        )
        self.assertRedirects(response, reverse('labels:list'))
        self.assertFalse(Label.objects.filter(id=label.id).exists())

    def test_unique_name_validation(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('labels:create'), {'name': 'bug'})
        self.assertEqual(response.status_code, 200)
        content = response.content.decode()
        self.assertTrue(
            'already exists' in content or 'уже существует' in content
        )

    def test_delete_label_associated_with_task(self):
        self.client.login(username='testuser', password='12345')
        task = Task.objects.create(
            name='Задача с меткой',
            status=Status.objects.get(pk=1),
            author=self.user,
        )
        task.labels.add(self.label)
        response = self.client.post(
            reverse('labels:delete', args=[self.label.id]), follow=True
        )
        self.assertRedirects(response, reverse('labels:list'))
        self.assertTrue(Label.objects.filter(id=self.label.id).exists())
        messages = list(response.context['messages'])
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Невозможно удалить метку')