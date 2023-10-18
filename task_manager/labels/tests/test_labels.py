from django.test import Client, TestCase
from django.urls import reverse_lazy

from task_manager.users.models import User
from task_manager.labels.models import Label


class LabelListTest(TestCase):
    fixtures = ['users.json', 'labels.json']
    client = Client
    page = str(reverse_lazy('labels_list'))
    login_page = str(reverse_lazy('login_user'))

    @classmethod
    def setUpTestData(cls):
        cls.labels = Label.objects

    def test_labels_list(self):
        self.client.force_login(User.objects.get(id=1))
        response = self.client.get(self.page)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.page, response.request['PATH_INFO'])
        received_labels = response.context_data['labels']
        all_labels = self.labels.all()
        for label in received_labels:
            self.assertTrue(label in all_labels)
            self.assertTrue(self.labels.filter(id=label.id).count() == 1)
        self.assertTrue(self.labels.count() == received_labels.count())

    def test_label_list_without_authorize(self):
        response = self.client.get(self.page)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.page, response.request['PATH_INFO'])
