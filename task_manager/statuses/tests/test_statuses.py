from django.test import Client, TestCase
from django.urls import reverse_lazy

from task_manager.users.models import User
from task_manager.statuses.models import Status


class StatusListTest(TestCase):
    fixtures = ['users.json', 'statuses.json']
    client = Client
    page = str(reverse_lazy('statuses_list'))
    login_page = str(reverse_lazy('login_user'))

    @classmethod
    def setUpTestData(cls):
        cls.statuses = Status.objects

    def test_statuses_list(self):
        self.client.force_login(User.objects.get(id=1))
        response = self.client.get(self.page)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.page, response.request['PATH_INFO'])
        received_statuses = response.context_data['statuses']
        all_statuses = self.statuses.all()
        for status in received_statuses:
            self.assertTrue(status in all_statuses)
            self.assertTrue(self.statuses.filter(id=status.id).count() == 1)
        self.assertTrue(self.statuses.count() == received_statuses.count())

    def test_status_list_without_authorize(self):
        response = self.client.get(self.page)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.page, response.request['PATH_INFO'])
