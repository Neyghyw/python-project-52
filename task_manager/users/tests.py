from django.test import TestCase, Client
from django.urls import reverse_lazy


# Create your tests here.
class Test(TestCase):
    user_data = {'first_name': 'Владислав',
                 'last_name': 'Цыганов',
                 'username': 'vlad',
                 'password1': 'Vlados123',
                 'password2': 'Vlados123'
                 }

    def test_create_user(self):
        client = Client()
        url = reverse_lazy("create_user")
        response = client.post(url, self.user_data)
        self.assertEqual(302, response.status_code, "Bad response status code.")
