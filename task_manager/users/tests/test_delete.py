from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse_lazy

from .custom_test_client import CustomTestClient


class DeleteUserTest(TestCase):
    fixtures = ['users.json']
    client = Client()

    @classmethod
    def setUpTestData(cls):
        cls.users = User.objects
        cls.users_in_fixture = cls.users.count()

    def send_delete_request(self, pk):
        url = reverse_lazy("delete_user", kwargs={'pk': pk})
        return self.client.post(url)

    def check_users_count(self, required_quantity):
        self.assertEqual(self.users.count(), required_quantity)

    def test_delete_user(self):
        user = self.users.get(id=1)
        self.client.force_login(user)
        response = self.send_delete_request(pk=1)
        self.check_users_count(self.users_in_fixture - 1)
        last_user = self.users.first()
        self.assertTrue(last_user.id == 2)
        message = 'Success! Chosen user was deleted.'
        message_presence = CustomTestClient.check_message(response, message)
        self.assertTrue(message_presence)

    def test_delete_another_user(self):
        first_user = self.users.get(id=1)
        self.client.force_login(first_user)
        response = self.send_delete_request(pk=2)
        self.check_users_count(self.users_in_fixture)
        message = 'Access granted only for authorized owner.'
        message_presence = CustomTestClient.check_message(response, message)
        self.assertTrue(message_presence)

    def test_delete_user_without_authorize(self):
        self.send_delete_request(pk=1)
        self.check_users_count(self.users_in_fixture)
