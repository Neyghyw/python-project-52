from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse_lazy
from tasks.models import Task
from .custom_test_client import CustomTestClient


class CreateTaskTest(TestCase):
    fixtures = ['users.json', 'statuses.json']
    client_class = CustomTestClient

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.get(id=1)
        cls.tasks = Task.objects
        cls.url = reverse_lazy("create_task")

    def check_tasks_count(self, required_quantity):
        self.assertEqual(self.tasks.count(), required_quantity)

    def test_create_task(self):
        self.client.force_login(self.user)
        self.client.send_post(self.url)
        self.check_tasks_count(1)

    def test_create_task_without_authorize(self):
        self.client.send_post(self.url)
        self.check_tasks_count(0)

    def test_new_task_have_required_data(self):
        self.client.force_login(self.user)
        response = self.client.send_post(self.url)
        form_data = self.client_class.form_data
        new_task = self.tasks.get(id=1)
        self.assertEqual(new_task.name, form_data['name'])
        self.assertEqual(new_task.description, form_data['description'])
        self.assertEqual(new_task.status.id, form_data['status'])
        self.assertEqual(new_task.executor.id, form_data['executor'])
        self.assertEqual(new_task.creator.id, 1)
        message = 'Success! New task was created.'
        message_presence = self.client.check_message(response, message)
        self.assertTrue(message_presence)

    def test_create_existing_task(self):
        self.client.force_login(self.user)
        self.client.send_post(self.url)
        self.client.send_post(self.url)
        self.check_tasks_count(1)
