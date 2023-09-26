from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse_lazy

from labels.models import Label

from .labels_test_client import LabelsTestClient


class DeleteLabelTest(TestCase):
    fixtures = ['users.json', 'tasks.json', 'labels.json', 'statuses.json']
    client_class = LabelsTestClient
    redirect_page = reverse_lazy("labels_list")

    @classmethod
    def setUpTestData(cls):
        cls.labels = Label.objects
        cls.labels_in_fixture = cls.labels.count()
        cls.user = User.objects.get(id=1)

    def send_delete_label_request(self, pk):
        url = reverse_lazy("delete_label", kwargs={'pk': pk})
        return self.client.send_post(url, with_form_data=False)

    def check_labels_count(self, required_quantity):
        return self.labels.count() == required_quantity

    def test_delete_label(self):
        label_owner = self.user
        self.client.force_login(label_owner)
        response = self.send_delete_label_request(pk=2)
        good_quantity = self.labels_in_fixture-1
        is_quantity_good = self.check_labels_count(good_quantity)
        self.assertTrue(is_quantity_good)
        last_label = self.labels.all().first()
        self.assertTrue(last_label.id == 1)
        self.assertEqual(response['Location'], self.redirect_page)
        message = 'Success! Chosen label was deleted.'
        message_presence = LabelsTestClient.check_message(response, message)
        self.assertTrue(message_presence)

    def test_delete_label_with_task(self):
        self.client.force_login(self.user)
        response = self.send_delete_label_request(pk=1)
        self.assertEqual(self.labels.count(), self.labels_in_fixture)
        message = ("Operation isn't possible."
                   " This label linked with exist task.")
        message_presence = self.client.check_message(response, message)
        self.assertTrue(message_presence)

    def test_delete_label_without_authorize(self):
        response = self.send_delete_label_request(pk=1)
        is_quantity_good = self.check_labels_count(self.labels_in_fixture)
        self.assertTrue(is_quantity_good)
        login_url = str(reverse_lazy("login_user"))
        redirect_location = str(response['Location'])
        self.assertTrue(login_url in redirect_location)
