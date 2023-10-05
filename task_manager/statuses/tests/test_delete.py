from django.test import TestCase
from django.urls import reverse_lazy

from task_manager.statuses.models import Status
from task_manager.users.models import User

from .statuses_test_client import StatusesTestClient


class DeleteStatusTest(TestCase):
    fixtures = ['statuses.json', 'users.json', 'tasks.json', 'labels.json']
    client_class = StatusesTestClient
    redirect_page = reverse_lazy('statuses_list')

    @classmethod
    def setUpTestData(cls):
        cls.statuses = Status.objects
        cls.statuses_in_fixture = cls.statuses.count()
        cls.user = User.objects.get(id=1)

    def send_delete_status_request(self, pk):
        url = reverse_lazy('delete_status', kwargs={'pk': pk})
        return self.client.send_post(url, with_form_data=False)

    def test_delete_status(self):
        self.client.force_login(self.user)
        response = self.send_delete_status_request(pk=3)
        self.assertEqual(self.statuses.count(), self.statuses_in_fixture - 1)
        self.assertEqual(response['Location'], self.redirect_page)
        message = 'Success! Chosen status was deleted.'
        message_presence = StatusesTestClient.check_message(response, message)
        self.assertTrue(message_presence)

    def test_delete_status_with_task(self):
        self.client.force_login(self.user)
        response = self.send_delete_status_request(pk=1)
        self.assertEqual(self.statuses.count(), self.statuses_in_fixture)
        message = ('Sorry, This object related with another table.'
                   ' Permission denied.')
        message_presence = StatusesTestClient.check_message(response, message)
        self.assertTrue(message_presence)

    def test_delete_status_without_authorize(self):
        response = self.send_delete_status_request(pk=3)
        self.assertEqual(self.statuses.count(), self.statuses_in_fixture)
        login_url = str(reverse_lazy('login_user'))
        redirect_location = str(response['Location'])
        self.assertTrue(login_url in redirect_location)
