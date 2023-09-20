from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse_lazy

from tasks.models import Task
from utils.test_utils import compare_dicts_and_assert


# # Create your tests here.
class CreateTaskTest(TestCase):
    fixtures = ['tasks/fixtures/user.json',
                'tasks/fixtures/statuses.json']

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.user = User.objects.get(id=1)
        cls.new_task_data = {'name': 'NewName',
                             'description': 'NewDescription',
                             'status': 1,
                             'executor': 2}

    def send_create_task_request(self, task_data):
        url = reverse_lazy("create_task")
        self.client.post(url, task_data)

    def test_create_task(self):
        self.client.force_login(self.user)
        self.send_create_task_request(self.new_task_data)
        self.assertEqual(Task.objects.count(), 1)

    def test_create_task_without_authorize(self):
        self.send_create_task_request(self.new_task_data)
        self.assertEqual(Task.objects.count(), 0)

    def test_new_task_have_required_data(self):
        required_data = self.new_task_data
        self.client.force_login(self.user)
        self.send_create_task_request(required_data)
        new_task_data = Task.objects.all().values().first()
        compare_dicts_and_assert(self, new_task_data, required_data)
        self.assertEqual(new_task_data['creator_id'], 1)

    def test_create_existing_task(self):
        self.client.force_login(self.user)
        self.send_create_task_request(self.new_task_data)
        self.send_create_task_request(self.new_task_data)
        error_text = "Test error. task created when already exist."
        self.assertEqual(Task.objects.count(), 1, error_text)


class DeleteTaskTest(TestCase):
    fixtures = ['tasks/fixtures/user.json',
                'tasks/fixtures/statuses.json',
                'tasks/fixtures/task.json']

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.user = User.objects.get(id=1)

    def send_delete_task_request(self, pk):
        url = reverse_lazy("delete_task", kwargs={'pk': pk})
        self.client.post(url)

    def test_delete_task(self):
        task_owner = self.user
        self.client.force_login(task_owner)
        self.send_delete_task_request(pk=1)
        self.assertEqual(Task.objects.count(), 0)

    def test_delete_task_without_owner(self):
        not_task_owner = User.objects.get(id=2)
        self.client.force_login(not_task_owner)
        self.send_delete_task_request(pk=1)
        self.assertEqual(Task.objects.count(), 1)

    def test_delete_task_without_authorize(self):
        self.send_delete_task_request(pk=1)
        self.assertEqual(Task.objects.count(), 1)


class UpdateTaskTest(TestCase):
    fixtures = ['tasks/fixtures/user.json',
                'tasks/fixtures/statuses.json',
                'tasks/fixtures/task.json']

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.task_update_data = {'name': 'UpdatedName',
                                'description': 'UpdatedDescription',
                                'status': 1,
                                'executor': 1}
        cls.user = User.objects.get(id=1)

    def send_update_task_request(self, pk):
        url = reverse_lazy("update_task", kwargs={'pk': pk})
        self.client.post(url, self.task_update_data)

    def test_update_task(self):
        task_owner = self.user
        self.client.force_login(task_owner)
        self.send_update_task_request(pk=1)
        task_dict = Task.objects.filter(id=1).values().first()
        compare_dicts_and_assert(self, task_dict, self.task_update_data)

    def test_update_task_without_owner(self):
        not_task_owner = self.user
        self.client.force_login(not_task_owner)
        task_before_update = Task.objects.get(id=1)
        self.send_update_task_request(pk=1)
        task_after_update = Task.objects.get(id=1)
        self.assertEqual(task_before_update, task_after_update)

    def test_update_with_unauthorized_request(self):
        self.send_update_task_request(pk=1)
        task = Task.objects.get(id=1)
        self.assertTrue(task.name != self.task_update_data['name'])
