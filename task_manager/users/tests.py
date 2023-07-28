from django.test import TestCase, Client
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

from utils.test_utils import compare_dicts_and_assert


# Create your tests here.
class CreateUserTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.create_url = reverse_lazy("create_user")
        cls.new_user_data = {'first_name': 'Johny',
                             'last_name': 'Walker',
                             'username': 'blacklabel',
                             'password1': '041048Q2001',
                             'password2': '041048Q2001'
                             }
        cls.weak_password = 'qwerty123'

    def send_create_user_request(self, user_data):
        url = reverse_lazy("create_user")
        self.client.post(url, user_data)

    def test_create_user(self):
        self.send_create_user_request(self.new_user_data)
        self.assertEqual(User.objects.count(), 1)

    def test_new_user_have_required_data(self):
        required_data = self.new_user_data
        self.send_create_user_request(required_data)
        new_user_data = User.objects.all().values().first()
        compare_dicts_and_assert(self, new_user_data, required_data)
        required_password = required_data['password1']
        fetched_password_hash = new_user_data['password']
        is_passwords_equal = check_password(required_password, fetched_password_hash)
        self.assertTrue(is_passwords_equal)

    def test_create_existing_user(self):
        self.send_create_user_request(self.new_user_data)
        self.send_create_user_request(self.new_user_data)
        error_text = "Test error. User created when already exist."
        self.assertEqual(User.objects.count(), 1, error_text)


class DeleteUserTest(TestCase):
    fixtures = ['users/fixtures/users.json']

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()

    def send_delete_user_request(self, pk):
        url = reverse_lazy("delete_user", kwargs={'pk': pk})
        self.client.post(url)

    def test_delete_user(self):
        users = User.objects
        user = users.get(id=1)
        self.client.force_login(user)
        self.send_delete_user_request(pk=user.id)
        self.assertEqual(users.count(), 1)
        last_user = users.first()
        self.assertEqual(last_user.id, 2)

    def test_delete_another_user(self):
        users = User.objects
        first_user = users.get(id=1)
        self.client.force_login(first_user)
        self.send_delete_user_request(pk=2)
        self.assertEqual(users.count(), 2)

    def test_delete_user_without_authorize(self):
        users = User.objects
        self.send_delete_user_request(pk=1)
        self.assertEqual(users.count(), 2)


class UpdateUserTest(TestCase):
    fixtures = ['users/fixtures/users.json']

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.user_update_data = {
            'first_name': 'Updated',
            'last_name': 'User',
            'username': 'updateduser',
            'password1': 'ItsSoCoolToBeUpdated123',
            'password2': 'ItsSoCoolToBeUpdated123'
        }

    def send_update_user_request(self, pk):
        url = reverse_lazy("update_user", kwargs={'pk': pk})
        self.client.post(url, self.user_update_data)

    def test_update_user(self):
        user = User.objects.get(id=1)
        self.client.force_login(user)
        self.send_update_user_request(pk=user.id)
        user_dict = User.objects.filter(id=1).values().first()
        compare_dicts_and_assert(self, user_dict, self.user_update_data)
        user_password_hash = user_dict['password']
        required_password = self.user_update_data['password1']
        is_passwords_equal = check_password(user_password_hash, required_password)
        self.assertTrue(is_passwords_equal)

    def test_update_with_unauthorized_request(self):
        old_user = User.objects.get(id=1)
        self.send_update_user_request(pk=old_user.id)
        updated_user = User.objects.get(id=1)
        self.assertEqual(updated_user, old_user)

    def test_update_another_user(self):
        users = User.objects
        user = users.get(id=1)
        self.client.force_login(user)
        another_user = users.get(id=2)
        self.send_update_user_request(pk=2)
        updated_another_user = users.get(id=2)
        self.assertEqual(updated_another_user, another_user)
