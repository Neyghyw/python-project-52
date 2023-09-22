from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse_lazy
from .custom_test_client import CustomTestClient


class UpdateUserTest(TestCase):
    fixtures = ['users.json']
    client_class = CustomTestClient

    @classmethod
    def setUpTestData(cls):
        cls.users = User.objects
        cls.user = cls.users.get(id=1)

    @staticmethod
    def get_url(pk):
        return reverse_lazy("update_user", kwargs={'pk': pk})

    def test_update_user(self):
        self.client.force_login(self.user)
        pk = self.user.id
        url = self.get_url(pk)
        response = self.client.send_post(url)

        form_data = self.client.form_data

        updated_user = self.users.get(id=1)
        self.assertEqual(updated_user.first_name, form_data['first_name'])
        self.assertEqual(updated_user.last_name, form_data['last_name'])
        self.assertEqual(updated_user.username, form_data['username'])
        self.assertTrue(check_password(form_data['password1'],
                                       updated_user.password))
        message = 'Success! User was updated.'
        message_presence = self.client.check_message(response, message)
        self.assertTrue(message_presence)

    def test_update_with_unauthorized_request(self):
        pk = self.user.id
        url = self.get_url(pk)
        response = self.client.send_post(url)
        updated_user = User.objects.get(id=pk)
        self.assertEqual(updated_user, self.user)  # message
        message = 'Access granted only for authorized owner.'
        message_presence = self.client.check_message(response, message)
        self.assertTrue(message_presence)

    def test_update_another_user(self):
        self.client.force_login(self.user)
        another_user = self.users.get(id=2)
        url = self.get_url(pk=2)
        self.client.send_post(url)
        another_user_after_update = self.users.get(id=2)
        self.assertEqual(another_user_after_update, another_user)
