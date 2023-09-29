from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse_lazy

from statuses.models import Status

from .statuses_test_client import StatusesTestClient


class UpdateStatusTest(TestCase):
    fixtures = ['statuses.json', 'users.json']
    client_class = StatusesTestClient
    url = reverse_lazy("update_status", kwargs={'pk': 1})
    redirect_page = reverse_lazy("statuses_list")

    @classmethod
    def setUpTestData(cls):
        cls.statuses = Status.objects
        cls.user = User.objects.get(id=1)

    def test_update_status(self):
        self.client.force_login(self.user)
        response = self.client.send_post(self.url)
        updated_status = self.statuses.get(id=1)
        form_data = self.client.form_data
        self.assertEqual(updated_status.name, form_data['name'])
        self.assertEqual(response['Location'], self.redirect_page)
        message = 'Success! Status was updated.'
        message_presence = self.client.check_message(response, message)
        self.assertTrue(message_presence)

    def test_update_with_unauthorized_request(self):
        old_status = self.statuses.get(id=1)
        response = self.client.send_post(self.url)
        status_after_update = self.statuses.get(id=1)
        self.assertEqual(old_status, status_after_update)
        login_url = str(reverse_lazy("login_user"))
        redirect_location = str(response['Location'])
        self.assertTrue(login_url in redirect_location)
