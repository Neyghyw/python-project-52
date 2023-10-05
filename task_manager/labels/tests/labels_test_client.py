from task_manager.utils.custom_test_client import CustomTestClient


class LabelsTestClient(CustomTestClient):
    form_data = {
        'name': 'NewName',
    }
