from utils.custom_test_client import CustomTestClient


class UsersTestClient(CustomTestClient):
    form_data = {
        'first_name': 'User',
        'last_name': 'Tester',
        'username': 'usertester',
        'password1': '041048Q2001',
        'password2': '041048Q2001'
    }
