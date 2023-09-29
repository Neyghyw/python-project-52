from task_manager.users.models import User
from django.test import TestCase
from django.urls import reverse_lazy

from task_manager.tasks.models import Task

from .tasks_test_client import TasksTestClient


class UpdateTaskTest(TestCase):
    fixtures = ['users.json', 'statuses.json', 'tasks.json', 'labels.json']
    client_class = TasksTestClient
    redirect_page = reverse_lazy("tasks_list")

    @classmethod
    def setUpTestData(cls):
        cls.tasks = Task.objects
        cls.user = User.objects.get(id=1)

    def send_update_task_request(self, pk):
        url = reverse_lazy("update_task", kwargs={'pk': pk})
        return self.client.send_post(url)

    def test_update_task(self):
        task_owner = self.user
        self.client.force_login(task_owner)
        response = self.send_update_task_request(pk=1)
        form_data = self.client.form_data

        new_task = self.tasks.get(id=1)
        self.assertEqual(new_task.name, form_data['name'])
        self.assertEqual(new_task.description, form_data['description'])
        self.assertEqual(new_task.status.id, form_data['status'])
        self.assertEqual(new_task.executor.id, form_data['executor'])
        self.assertEqual(new_task.creator.id, 1)
        self.assertEqual(response['Location'], self.redirect_page)
        message = 'Success! Task was updated.'
        message_presence = self.client.check_message(response, message)
        self.assertTrue(message_presence)

    def test_update_task_without_owner(self):
        not_task_owner = User.objects.get(id=2)
        self.client.force_login(not_task_owner)
        task = self.tasks.get(id=1)
        response = self.send_update_task_request(pk=1)
        task_after_update = self.tasks.get(id=1)
        self.assertEqual(task, task_after_update)
        message = 'Access granted only for owner.'
        message_presence = self.client.check_message(response, message)
        self.assertTrue(message_presence)

    def test_update_with_unauthorized_request(self):
        task = self.tasks.get(id=1)
        response = self.send_update_task_request(pk=1)
        task_after_update = self.tasks.get(id=1)
        self.assertEqual(task, task_after_update)
        login_url = str(reverse_lazy("login_user"))
        redirect_location = str(response['Location'])
        self.assertTrue(login_url in redirect_location)
