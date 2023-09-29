from django.contrib.messages import get_messages
from django.test import Client


class CustomTestClient(Client):

    form_data = None

    def send_post(self, url, with_form_data=True):
        if not with_form_data:
            return self.post(url)
        return self.post(url, self.form_data)

    @staticmethod
    def check_message(response, message):
        messages = list(get_messages(response.wsgi_request))
        count_good = len(messages) == 1
        if not messages and count_good:
            return False
        message_good = str(messages[0]) == message
        return message_good and count_good
