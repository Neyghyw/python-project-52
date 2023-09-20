from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse_lazy

from statuses.models import Status
from utils.test_utils import compare_dicts_and_assert


# # Create your tests here.
class CreateStatusTest(TestCase):
    fixtures = ['statuses/fixtures/user.json']

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.user = User.objects.get(id=1)
        cls.new_status_data = {'name': 'NameStatus'}

    def send_create_status_request(self, status_data):
        url = reverse_lazy("create_status")
        self.client.post(url, status_data)

    def test_create_status(self):
        self.client.force_login(self.user)
        self.send_create_status_request(self.new_status_data)
        self.assertEqual(Status.objects.count(), 1)

    def test_create_status_without_authorize(self):
        self.send_create_status_request(self.new_status_data)
        self.assertEqual(Status.objects.count(), 0)

    def test_new_status_have_required_data(self):
        required_data = self.new_status_data
        self.client.force_login(self.user)
        self.send_create_status_request(required_data)
        new_status_data = Status.objects.all().values().first()
        compare_dicts_and_assert(self, new_status_data, required_data)

    def test_create_existing_status(self):
        self.client.force_login(self.user)
        self.send_create_status_request(self.new_status_data)
        self.send_create_status_request(self.new_status_data)
        error_text = "Test error. status created when already exist."
        self.assertEqual(Status.objects.count(), 1, error_text)


class DeleteStatusTest(TestCase):
    fixtures = ['statuses/fixtures/statuses.json',
                'statuses/fixtures/user.json']

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.user = User.objects.get(id=1)

    def send_delete_status_request(self, pk):
        url = reverse_lazy("delete_status", kwargs={'pk': pk})
        self.client.post(url)

    def test_delete_status(self):
        self.client.force_login(self.user)
        self.send_delete_status_request(pk=1)
        self.assertEqual(Status.objects.count(), 0)

    def test_delete_status_with_task(self):  # ДОПИЛИТЬ ПРОВЕРКУ С ЗАДАЧЕЙ
        self.client.force_login(self.user)
        self.assertTrue(True)

    def test_delete_status_without_authorize(self):
        self.send_delete_status_request(pk=1)
        self.assertEqual(Status.objects.count(), 1)


class UpdateStatusTest(TestCase):
    fixtures = ['statuses/fixtures/statuses.json',
                'statuses/fixtures/user.json']

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.status_update_data = {'name': 'UpdatedName'}
        cls.user = User.objects.get(id=1)

    def send_update_status_request(self, pk):
        url = reverse_lazy("update_status", kwargs={'pk': pk})
        self.client.post(url, self.status_update_data)

    def test_update_status(self):
        self.client.force_login(self.user)
        self.send_update_status_request(pk=1)
        status_dict = Status.objects.filter(id=1).values().first()
        compare_dicts_and_assert(self, status_dict, self.status_update_data)

    def test_update_with_unauthorized_request(self):
        self.send_update_status_request(pk=1)
        status = Status.objects.get(id=1)
        self.assertTrue(status.name != self.status_update_data['name'])
