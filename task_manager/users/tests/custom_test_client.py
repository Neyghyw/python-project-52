from django.test import Client
from django.contrib.messages import get_messages


class CustomTestClient(Client):
    form_data = {'first_name': 'User',
                 'last_name': 'Tester',
                 'username': 'usertester',
                 'password1': '041048Q2001',
                 'password2': '041048Q2001'}

    def send_post(self, url):
        return self.post(url, self.form_data)

    @staticmethod
    def check_message(response, message):
        messages = list(get_messages(response.wsgi_request))
        print(messages[0])
        count_good = len(messages) == 1
        if not messages and count_good:
            return False
        message_good = str(messages[0]) == message
        return message_good and count_good
