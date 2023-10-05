from django.test import TestCase
from django.urls import reverse_lazy

from task_manager.labels.models import Label
from task_manager.users.models import User

from .labels_test_client import LabelsTestClient


class UpdateLabelTest(TestCase):
    fixtures = ['users.json', 'labels.json']
    client_class = LabelsTestClient
    redirect_page = reverse_lazy('labels_list')

    @classmethod
    def setUpTestData(cls):
        cls.labels = Label.objects
        cls.user = User.objects.get(id=1)

    def send_update_label_request(self, pk):
        url = reverse_lazy('update_label', kwargs={'pk': pk})
        return self.client.send_post(url)

    def test_update_label(self):
        label_owner = self.user
        self.client.force_login(label_owner)
        response = self.send_update_label_request(pk=1)
        form_data = self.client.form_data

        new_label = self.labels.get(id=1)
        self.assertEqual(new_label.name, form_data['name'])
        self.assertEqual(response['Location'], self.redirect_page)
        message = 'Success! Label was updated.'
        message_presence = self.client.check_message(response, message)
        self.assertTrue(message_presence)

    def test_update_with_unauthorized_request(self):
        label = self.labels.get(id=1)
        response = self.send_update_label_request(pk=1)
        label_after_update = self.labels.get(id=1)
        self.assertEqual(label, label_after_update)
        login_url = str(reverse_lazy('login_user'))
        redirect_location = str(response['Location'])
        self.assertTrue(login_url in redirect_location)
