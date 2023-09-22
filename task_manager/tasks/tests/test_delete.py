from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse_lazy
from tasks.models import Task
from .custom_test_client import CustomTestClient


class DeleteTaskTest(TestCase):
    fixtures = ['users.json', 'statuses.json', 'tasks.json']
    client = Client()

    @classmethod
    def setUpTestData(cls):
        cls.tasks = Task.objects
        cls.tasks_in_fixture = cls.tasks.count()
        cls.user = User.objects.get(id=1)

    def send_delete_task_request(self, pk):
        url = reverse_lazy("delete_task", kwargs={'pk': pk})
        return self.client.post(url)

    def check_tasks_count(self, required_quantity):
        self.assertEqual(self.tasks.count(), required_quantity)

    def test_delete_task(self):
        task_owner = self.user
        self.client.force_login(task_owner)
        response = self.send_delete_task_request(pk=1)
        self.check_tasks_count(self.tasks_in_fixture - 1)
        last_task = self.tasks.all().first()
        self.assertTrue(last_task.id == 2)
        message = 'Success! Chosen task was deleted.'
        message_presence = CustomTestClient.check_message(response, message)
        self.assertTrue(message_presence)

    def test_delete_task_without_owner(self):
        not_task_owner = User.objects.get(id=2)
        self.client.force_login(not_task_owner)
        response = self.send_delete_task_request(pk=1)
        self.check_tasks_count(self.tasks_in_fixture)
        message = 'Access granted only for owner.'
        message_presence = CustomTestClient.check_message(response, message)
        self.assertTrue(message_presence)

    def test_delete_task_without_authorize(self):
        self.send_delete_task_request(pk=1)
        self.check_tasks_count(self.tasks_in_fixture)
