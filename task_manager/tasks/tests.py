from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse_lazy

from tasks.models import Task


# # Create your tests here.
class CreateTaskTest(TestCase):
    fixtures = ['users.json', 'statuses.json']

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.user = User.objects.get(id=1)
        cls.tasks = Task.objects
        cls.create_data = {'name': 'NewName',
                           'description': 'NewDescription',
                           'status': 1,
                           'executor': 2}

    def send_create_task_request(self):
        url = reverse_lazy("create_task")
        self.client.post(url, self.create_data)

    def check_tasks_count(self, required_quantity):
        self.assertEqual(self.tasks.count(), required_quantity)

    def test_create_task(self):
        self.client.force_login(self.user)
        self.send_create_task_request()
        self.check_tasks_count(1)

    def test_create_task_without_authorize(self):
        self.send_create_task_request()
        self.check_tasks_count(0)

    def test_new_task_have_required_data(self):
        self.client.force_login(self.user)
        self.send_create_task_request()
        created_task = self.tasks.get(id=1)
        required_name = self.create_data['name']
        required_description = self.create_data['description']
        required_status = self.create_data['status']
        required_executor = self.create_data['executor']
        self.assertEqual(created_task.name, required_name)
        self.assertEqual(created_task.description, required_description)
        self.assertEqual(created_task.status.id, required_status)
        self.assertEqual(created_task.executor.id, required_executor)
        self.assertEqual(created_task.creator.id, 1)

    def test_create_existing_task(self):
        self.client.force_login(self.user)
        self.send_create_task_request()
        self.send_create_task_request()
        self.check_tasks_count(1)


class UpdateTaskTest(TestCase):
    fixtures = ['users.json', 'statuses.json', 'tasks.json']

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.tasks = Task.objects
        cls.user = User.objects.get(id=1)
        cls.update_data = {'name': 'UpdatedName',
                           'description': 'UpdatedDescription',
                           'status': 1,
                           'executor': 1}

    def send_update_task_request(self, pk):
        url = reverse_lazy("update_task", kwargs={'pk': pk})
        self.client.post(url, self.update_data)

    def test_update_task(self):
        task_owner = self.user
        self.client.force_login(task_owner)
        self.send_update_task_request(pk=1)
        updated_task = self.tasks.get(id=1)
        required_name = self.update_data['name']
        required_description = self.update_data['description']
        required_status = self.update_data['status']
        required_executor = self.update_data['executor']
        self.assertEqual(updated_task.name, required_name)
        self.assertEqual(updated_task.description, required_description)
        self.assertEqual(updated_task.status.id, required_status)
        self.assertEqual(updated_task.executor.id, required_executor)
        self.assertEqual(updated_task.creator.id, 1)

    def test_update_task_without_owner(self):
        not_task_owner = User.objects.get(id=2)
        self.client.force_login(not_task_owner)
        task = self.tasks.get(id=1)
        self.send_update_task_request(pk=1)
        task_after_update = self.tasks.get(id=1)
        self.assertEqual(task, task_after_update)

    def test_update_with_unauthorized_request(self):
        task = self.tasks.get(id=1)
        self.send_update_task_request(pk=1)
        task_after_update = self.tasks.get(id=1)
        self.assertEqual(task, task_after_update)


class DeleteTaskTest(TestCase):
    fixtures = ['users.json', 'statuses.json', 'tasks.json']

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.tasks = Task.objects
        cls.tasks_in_fixture = cls.tasks.count()
        cls.user = User.objects.get(id=1)

    def send_delete_task_request(self, pk):
        url = reverse_lazy("delete_task", kwargs={'pk': pk})
        self.client.post(url)

    def check_tasks_count(self, required_quantity):
        self.assertEqual(self.tasks.count(), required_quantity)

    def test_delete_task(self):
        task_owner = self.user
        self.client.force_login(task_owner)
        self.send_delete_task_request(pk=1)
        self.check_tasks_count(self.tasks_in_fixture - 1)
        last_task = self.tasks.all().first()
        self.assertTrue(last_task.id == 2)

    def test_delete_task_without_owner(self):
        not_task_owner = User.objects.get(id=2)
        self.client.force_login(not_task_owner)
        self.send_delete_task_request(pk=1)
        self.check_tasks_count(self.tasks_in_fixture)

    def test_delete_task_without_authorize(self):
        self.send_delete_task_request(pk=1)
        self.check_tasks_count(self.tasks_in_fixture)
