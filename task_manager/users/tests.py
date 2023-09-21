from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.test import Client, TestCase
from django.urls import reverse_lazy


# Create your tests here.
class CreateUserTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.create_url = reverse_lazy("create_user")
        cls.weak_password = 'qwerty123'
        cls.data_for_create = {'first_name': 'User',
                               'last_name': 'Tester',
                               'username': 'usertester',
                               'password1': '041048Q2001',
                               'password2': '041048Q2001'}

    def send_create_user_request(self):
        url = reverse_lazy("create_user")
        self.client.post(url, self.data_for_create)

    def test_create_user(self):
        self.send_create_user_request()
        self.assertEqual(User.objects.count(), 1)

    def test_new_user_have_required_data(self):
        self.send_create_user_request()
        created_user = User.objects.first()

        required_first_name = self.data_for_create['first_name']
        required_last_name = self.data_for_create['last_name']
        required_username = self.data_for_create['username']
        required_password = self.data_for_create['password1']

        self.assertEqual(created_user.first_name, required_first_name)
        self.assertEqual(created_user.last_name, required_last_name)
        self.assertEqual(created_user.username, required_username)
        self.assertTrue(check_password(required_password,
                                       created_user.password))

    def test_create_existing_user(self):
        self.send_create_user_request()
        self.send_create_user_request()
        error_text = "Test error. User created when already exist."
        self.assertEqual(User.objects.count(), 1, error_text)


class DeleteUserTest(TestCase):
    fixtures = ['users.json']

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.users = User.objects
        cls.users_in_fixture = cls.users.count()

    def check_users_count(self, required_quantity):
        self.assertEqual(self.users.count(), required_quantity)

    def send_delete_user_request(self, pk):
        url = reverse_lazy("delete_user", kwargs={'pk': pk})
        self.client.post(url)

    def test_delete_user(self):
        user = self.users.get(id=1)
        self.client.force_login(user)
        self.send_delete_user_request(pk=user.id)
        required_users_quantity = self.users_in_fixture - 1
        self.check_users_count(required_users_quantity)
        last_user = self.users.first()
        self.assertTrue(last_user.id == 2)

    def test_delete_another_user(self):
        first_user = self.users.get(id=1)
        self.client.force_login(first_user)
        second_user_id = 2
        self.send_delete_user_request(pk=second_user_id)
        required_users_quantity = self.users_in_fixture
        self.check_users_count(required_users_quantity)

    def test_delete_user_without_authorize(self):
        self.send_delete_user_request(pk=1)
        required_users_quantity = self.users_in_fixture
        self.check_users_count(required_users_quantity)


class UpdateUserTest(TestCase):
    fixtures = ['users.json']

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.users = User.objects
        cls.user = cls.users.get(id=1)
        cls.data_for_update = {
            'first_name': 'Updated',
            'last_name': 'User',
            'username': 'updateduser',
            'password1': 'ItsSoCoolToBeUpdated123',
            'password2': 'ItsSoCoolToBeUpdated123'
        }

    def send_update_user_request(self, pk):
        url = reverse_lazy("update_user", kwargs={'pk': pk})
        self.client.post(url, self.data_for_update)

    def test_update_user(self):
        self.client.force_login(self.user)
        self.send_update_user_request(pk=self.user.id)
        updated_user = self.users.get(id=1)

        required_first_name = self.data_for_update['first_name']
        required_last_name = self.data_for_update['last_name']
        required_username = self.data_for_update['username']
        required_password = self.data_for_update['password1']

        self.assertEqual(updated_user.first_name, required_first_name)
        self.assertEqual(updated_user.last_name, required_last_name)
        self.assertEqual(updated_user.username, required_username)
        self.assertTrue(check_password(required_password,
                                       updated_user.password))

    def test_update_with_unauthorized_request(self):
        self.send_update_user_request(pk=self.user.id)
        updated_user = User.objects.get(id=1)
        self.assertEqual(updated_user, self.user)

    def test_update_another_user(self):
        self.client.force_login(self.user)
        user_old = self.users.get(id=2)
        self.send_update_user_request(pk=2)
        user_after_update = self.users.get(id=2)
        self.assertEqual(user_after_update, user_old)
