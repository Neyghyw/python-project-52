from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse_lazy

from tasks.models import Task

from .tasks_test_client import TasksTestClient


class CreateTaskTest(TestCase):
    fixtures = ['users.json', 'statuses.json', 'labels.json']
    client_class = TasksTestClient
    redirect_page = reverse_lazy("tasks_list")

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.get(id=1)
        cls.tasks = Task.objects
        cls.url = reverse_lazy("create_task")

    def check_tasks_count(self, required_quantity):
        return self.tasks.count() == required_quantity

    def test_create_task(self):
        self.client.force_login(self.user)
        response = self.client.send_post(self.url)
        is_quantity_good = self.check_tasks_count(1)
        self.assertTrue(is_quantity_good)
        self.assertEqual(response['Location'], self.redirect_page)

    def test_create_task_without_authorize(self):
        response = self.client.send_post(self.url)
        login_url = str(reverse_lazy("login_user"))
        redirect_location = str(response['Location'])
        is_quantity_good = self.check_tasks_count(0)
        self.assertTrue(is_quantity_good)
        self.assertTrue(login_url in redirect_location)

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
        is_quantity_good = self.check_tasks_count(1)
        self.assertTrue(is_quantity_good)
