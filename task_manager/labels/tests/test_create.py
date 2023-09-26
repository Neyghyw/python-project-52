from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse_lazy

from labels.models import Label

from labels.tests.labels_test_client import LabelsTestClient


class CreateLabelTest(TestCase):
    fixtures = ['users.json']
    client_class = LabelsTestClient
    redirect_page = reverse_lazy("labels_list")

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.get(id=1)
        cls.labels = Label.objects
        cls.url = reverse_lazy("create_label")

    def check_labels_count(self, required_quantity):
        self.assertEqual(self.labels.count(), required_quantity)

    def test_create_label(self):
        self.client.force_login(self.user)
        response = self.client.send_post(self.url)
        self.check_labels_count(1)
        self.assertEqual(response['Location'], self.redirect_page)

    def test_create_label_without_authorize(self):
        response = self.client.send_post(self.url)
        login_url = str(reverse_lazy("login_user"))
        redirect_location = str(response['Location'])
        self.check_labels_count(0)
        self.assertTrue(login_url in redirect_location)

    def test_new_label_have_required_data(self):
        self.client.force_login(self.user)
        response = self.client.send_post(self.url)
        form_data = self.client_class.form_data
        new_label = self.labels.get(id=1)
        self.assertEqual(new_label.name, form_data['name'])
        message = 'Success! New label was created.'
        message_presence = self.client.check_message(response, message)
        self.assertTrue(message_presence)

    def test_create_existing_label(self):
        self.client.force_login(self.user)
        self.client.send_post(self.url)
        self.client.send_post(self.url)
        self.check_labels_count(1)
