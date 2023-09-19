from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy


class UserAccessMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        user_id = request.user.id
        manipulated_object_id = kwargs.get('pk')
        if manipulated_object_id != user_id:
            message_text = 'Access granted only for authorized owner.'
            messages.add_message(request, messages.ERROR, message_text)
            return redirect(reverse_lazy('users_list'))
        return super().dispatch(request, *args, **kwargs)
