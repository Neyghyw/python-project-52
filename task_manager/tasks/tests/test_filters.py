from task_manager.users.models import User
from django.test import Client, TestCase
from django.urls import reverse_lazy

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task


class CreateTaskTest(TestCase):
    fixtures = ['users.json', 'statuses.json', 'labels.json', 'tasks.json']
    client = Client
    redirect_page = reverse_lazy("tasks_list")
    user = User.objects.get(id=1)

    @classmethod
    def setUpTestData(cls):
        cls.tasks = Task.objects

    def setUp(self):
        self.client.force_login(self.user)

    def test_filter_by_status(self):
        status = Status.objects.get(id=1)
        required_tasks = Task.objects.filter(status=status)
        url = f'{self.redirect_page}?status=1'
        response = self.client.get(url)
        received_tasks = response.context['tasks']
        self.assertEqual(response.status_code, 200)
        self.assertSetEqual(received_tasks, required_tasks)

    def test_filter_by_label(self):
        label = Label.objects.get(id=1)
        required_tasks = Task.objects.filter(label=label)
        url = f'{self.redirect_page}?label=1'
        response = self.client.get(url)
        received_tasks = response.context['tasks']
        self.assertEqual(response.status_code, 200)
        self.assertSetEqual(received_tasks, required_tasks)

    def test_filter_by_executor(self):
        required_tasks = Task.objects.filter(executor=self.user)
        url = f'{self.redirect_page}?executor=1'
        response = self.client.get(url)
        received_tasks = response.context['tasks']
        self.assertEqual(response.status_code, 200)
        self.assertSetEqual(received_tasks, required_tasks)

    def test_filter_self_tasks(self):
        required_tasks = Task.objects.filter(creator=self.user)
        url = f'{self.redirect_page}?self_tasks=on'
        response = self.client.get(url)
        received_tasks = response.context['tasks']
        self.assertEqual(response.status_code, 200)
        self.assertSetEqual(received_tasks, required_tasks)

    def test_multi_filter(self):
        label = Label.objects.get(id=1)
        status = Status.objects.get(id=1)
        executor = User.objects.get(id=2)
        required_tasks = Task.objects.filter(creator=self.user,
                                             label=label,
                                             status=status,
                                             executor=executor)
        url = f'{self.redirect_page}?status=1&executor=2&label=1&self_tasks=on'  # noqa: E501
        response = self.client.get(url)
        received_tasks = response.context['tasks']
        self.assertEqual(response.status_code, 200)
        self.assertSetEqual(received_tasks, required_tasks)
