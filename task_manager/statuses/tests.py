from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse_lazy
from utils.test_utils import compare_dicts_and_assert

from statuses.models import Status


# # Create your tests here.
class CreateStatusTest(TestCase):
    fixtures = ['users.json']

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.statuses = Status.objects
        cls.user = User.objects.get(id=1)
        cls.data_for_create = {'name': 'NameStatus'}

    def send_create_status_request(self):
        url = reverse_lazy("create_status")
        self.client.post(url, self.data_for_create)

    def test_create_status(self):
        self.client.force_login(self.user)
        self.send_create_status_request()
        self.assertEqual(self.statuses.count(), 1)

    def test_create_status_without_authorize(self):
        self.send_create_status_request()
        self.assertEqual(self.statuses.count(), 0)

    def test_new_status_have_required_data(self):
        self.client.force_login(self.user)
        self.send_create_status_request()
        created_status_dict = self.statuses.all().values().first()
        compare_dicts_and_assert(self, created_status_dict,
                                 self.data_for_create)

    def test_create_existing_status(self):
        self.client.force_login(self.user)
        self.send_create_status_request()
        self.send_create_status_request()
        self.assertEqual(self.statuses.count(), 1)


class DeleteStatusTest(TestCase):
    fixtures = ['statuses.json', 'users.json', 'tasks.json']

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.statuses = Status.objects
        cls.statuses_in_fixture = cls.statuses.count()
        cls.user = User.objects.get(id=1)

    def send_delete_status_request(self, pk):
        url = reverse_lazy("delete_status", kwargs={'pk': pk})
        self.client.post(url)

    def test_delete_status(self):
        self.client.force_login(self.user)
        self.send_delete_status_request(pk=3)
        self.assertEqual(self.statuses.count(), self.statuses_in_fixture - 1)

    def test_delete_status_with_task(self):
        self.client.force_login(self.user)
        self.send_delete_status_request(pk=1)
        self.assertEqual(self.statuses.count(), self.statuses_in_fixture)

    def test_delete_status_without_authorize(self):
        self.send_delete_status_request(pk=3)
        self.assertEqual(self.statuses.count(), self.statuses_in_fixture)


class UpdateStatusTest(TestCase):
    fixtures = ['statuses.json', 'users.json']

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.statuses = Status.objects
        cls.user = User.objects.get(id=1)
        cls.data_for_update = {'name': 'UpdatedName'}

    def send_update_status_request(self, pk):
        url = reverse_lazy("update_status", kwargs={'pk': pk})
        self.client.post(url, self.data_for_update)

    def test_update_status(self):
        self.client.force_login(self.user)
        self.send_update_status_request(pk=1)
        status_dict = self.statuses.filter(id=1).values().first()
        compare_dicts_and_assert(self, status_dict, self.data_for_update)

    def test_update_with_unauthorized_request(self):
        old_status = self.statuses.get(id=1)
        self.send_update_status_request(pk=1)
        status_after_update = self.statuses.get(id=1)
        self.assertEqual(old_status, status_after_update)
