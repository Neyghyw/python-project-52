from utils.custom_test_client import CustomTestClient


class StatusesTestClient(CustomTestClient):
    form_data = {
        'name': 'NameStatus'
    }
