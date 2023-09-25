from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse_lazy

from statuses.models import Status

from .statuses_test_client import StatusesTestClient


# # Create your tests here.
class CreateStatusTest(TestCase):
    fixtures = ['users.json']
    client_class = StatusesTestClient
    url = reverse_lazy("create_status")
    redirect_page = reverse_lazy("statuses_list")

    @classmethod
    def setUpTestData(cls):
        cls.statuses = Status.objects
        cls.user = User.objects.get(id=1)

    def test_create_status(self):
        self.client.force_login(self.user)
        response = self.client.send_post(self.url)
        self.assertEqual(self.statuses.count(), 1)
        self.assertEqual(response['Location'], self.redirect_page)
        message = 'Success! New status was created.'
        message_presence = self.client.check_message(response, message)
        self.assertTrue(message_presence)

    def test_create_status_without_authorize(self):
        response = self.client.send_post(self.url)
        self.assertEqual(self.statuses.count(), 0)
        login_url = str(reverse_lazy("login_user"))
        redirect_location = str(response['Location'])
        self.assertTrue(login_url in redirect_location)

    def test_new_status_have_required_data(self):
        self.client.force_login(self.user)
        self.client.send_post(self.url)
        new_status = self.statuses.first()
        form_data = self.client.form_data
        self.assertEqual(new_status.name, form_data['name'])

    def test_create_existing_status(self):
        self.client.force_login(self.user)
        self.client.send_post(self.url)
        self.client.send_post(self.url)
        self.assertEqual(self.statuses.count(), 1)
