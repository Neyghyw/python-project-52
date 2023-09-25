from utils.custom_test_client import CustomTestClient


class TasksTestClient(CustomTestClient):
    form_data = {
        'name': 'NewName',
        'description': 'NewDescription',
        'status': 1,
        'executor': 2
    }
