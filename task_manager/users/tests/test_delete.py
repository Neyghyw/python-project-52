from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse_lazy

from .users_test_client import UsersTestClient


class DeleteUserTest(TestCase):
    fixtures = ['users.json']
    client_class = UsersTestClient
    redirect_page = reverse_lazy("users_list")

    @classmethod
    def setUpTestData(cls):
        cls.users = User.objects
        cls.users_in_fixture = cls.users.count()

    def send_delete_user_request(self, pk):
        url = reverse_lazy("delete_user", kwargs={'pk': pk})
        return self.client.send_post(url, with_form_data=False)

    def check_users_count(self, required_quantity):
        self.assertEqual(self.users.count(), required_quantity)

    def test_delete_user(self):
        user = self.users.get(id=1)
        self.client.force_login(user)
        response = self.send_delete_user_request(pk=1)
        self.check_users_count(self.users_in_fixture - 1)
        last_user = self.users.first()
        self.assertTrue(last_user.id == 2)
        self.assertEqual(response['Location'], self.redirect_page)
        message = 'Success! Chosen user was deleted.'
        message_presence = UsersTestClient.check_message(response, message)
        self.assertTrue(message_presence)

    def test_delete_another_user(self):
        first_user = self.users.get(id=1)
        self.client.force_login(first_user)
        response = self.send_delete_user_request(pk=2)
        self.check_users_count(self.users_in_fixture)
        message = 'Access granted only for authorized owner.'
        message_presence = UsersTestClient.check_message(response, message)
        self.assertTrue(message_presence)

    def test_delete_user_without_authorize(self):
        response = self.send_delete_user_request(pk=1)
        self.check_users_count(self.users_in_fixture)
        self.assertEqual(response['Location'], self.redirect_page)
