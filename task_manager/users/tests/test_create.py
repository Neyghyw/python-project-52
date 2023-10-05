from django.contrib.auth.hashers import check_password
from django.test import TestCase
from django.urls import reverse_lazy

from task_manager.users.models import User

from .users_test_client import UsersTestClient


class CreateUserTest(TestCase):
    client_class = UsersTestClient
    url = reverse_lazy('create_user')
    redirect_page = reverse_lazy('login_user')

    def test_create_user(self):
        response = self.client.send_post(self.url)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['Location'], self.redirect_page)

    def test_new_user_have_required_data(self):
        response = self.client.send_post(self.url)
        form_data = self.client.form_data
        required_first_name = form_data['first_name']
        required_last_name = form_data['last_name']
        required_username = form_data['username']
        required_password = form_data['password1']
        new_user = User.objects.first()
        self.assertEqual(new_user.first_name, required_first_name)
        self.assertEqual(new_user.last_name, required_last_name)
        self.assertEqual(new_user.username, required_username)
        self.assertTrue(check_password(required_password, new_user.password))
        message = 'Success! User was created.'
        message_presence = self.client.check_message(response, message)
        self.assertTrue(message_presence)

    def test_create_existing_user(self):
        self.client.send_post(self.url)
        self.client.send_post(self.url)
        self.assertEqual(User.objects.count(), 1)
