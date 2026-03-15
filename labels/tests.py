from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from statuses.models import Status
from tasks.models import Task

from .models import Label


class LabelCRUDTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='12345'
            )
        self.label = Label.objects.create(name='Тестовая метка')

    def test_list_labels_not_logged_in(self):
        response = self.client.get(reverse('labels'))
        self.assertRedirects(
            response, f"{reverse('login')}?next={reverse('labels')}"
            )

    def test_list_labels_logged_in(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('labels'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Тестовая метка')

    def test_create_label_not_logged_in(self):
        response = self.client.get(reverse('label_create'))
        self.assertRedirects(
            response, f"{reverse('login')}?next={reverse('label_create')}"
            )

    def test_create_label_logged_in(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(
            reverse('label_create'), {'name': 'Новая метка'}
            )
        self.assertRedirects(response, reverse('labels'))
        self.assertTrue(Label.objects.filter(name='Новая метка').exists())

    def test_update_label(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(
            reverse(
                'label_update',
                args=[self.label.id]),
                {'name': 'Изменённая'}
            )
        self.assertRedirects(response, reverse('labels'))
        self.label.refresh_from_db()
        self.assertEqual(self.label.name, 'Изменённая')

    def test_delete_label_not_associated(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(
            reverse('label_delete', args=[self.label.id])
            )
        self.assertRedirects(response, reverse('labels'))
        self.assertFalse(Label.objects.filter(id=self.label.id).exists())

    def test_delete_label_associated_with_task(self):
        self.client.login(username='testuser', password='12345')
        status = Status.objects.create(name='Новый')
        task = Task.objects.create(
            name='Тестовая задача',
            status=status,
            author=self.user,
        )
        task.labels.add(self.label)
        response = self.client.post(
            reverse('label_delete', args=[self.label.id])
            )
        self.assertRedirects(response, reverse('labels'))
        self.assertTrue(Label.objects.filter(id=self.label.id).exists())
        messages = list(response.wsgi_request._messages)
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), 'Невозможно удалить метку')