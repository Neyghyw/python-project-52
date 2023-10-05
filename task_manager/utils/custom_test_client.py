from django.contrib.messages import get_messages
from django.test import Client
from django.utils.translation import gettext_lazy as _


class CustomTestClient(Client):

    form_data = None

    def send_post(self, url, with_form_data=True):
        if not with_form_data:
            return self.post(url)
        return self.post(url, self.form_data)

    @staticmethod
    def check_message(response, message):
        messages = list(get_messages(response.wsgi_request))
        if not messages:
            return False
        received_message = str(messages[0])
        message_good = received_message == _(message)
        return message_good
