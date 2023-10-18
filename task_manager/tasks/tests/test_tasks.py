from django.test import Client, TestCase
from django.urls import reverse_lazy

from task_manager.users.models import User
from task_manager.tasks.models import Task


class TaskListTest(TestCase):
    fixtures = ['users.json', 'statuses.json', 'labels.json', 'tasks.json']
    client = Client
    page = str(reverse_lazy('tasks_list'))
    login_page = str(reverse_lazy('login_user'))

    @classmethod
    def setUpTestData(cls):
        cls.tasks = Task.objects

    def test_task_list(self):
        self.client.force_login(User.objects.get(id=1))
        response = self.client.get(self.page)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.page, response.request['PATH_INFO'])
        received_tasks = response.context_data['tasks']
        all_tasks = self.tasks.all()
        for task in received_tasks:
            self.assertTrue(task in all_tasks)
            self.assertTrue(self.tasks.filter(id=task.id).count() == 1)
        self.assertTrue(self.tasks.count() == received_tasks.count())

    def test_task_list_without_authorize(self):
        response = self.client.get(self.page)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.page, response.request['PATH_INFO'])
