from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin


class UserAccessMixin(LoginRequiredMixin, AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        user_id = request.user.id
        manipulated_object_id = kwargs.get('pk')
        if manipulated_object_id != user_id:
            message_text = _('Access granted only for authorized owner.')
            messages.add_message(request, messages.ERROR, message_text)
            return redirect(reverse_lazy('users_list'))
        return super().dispatch(request, *args, **kwargs)
