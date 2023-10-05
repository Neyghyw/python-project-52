from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _


class TaskAccessMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        task = self.get_object()
        if task.creator != request.user:
            message_text = _('Access granted only for owner.')
            messages.error(request, message_text)
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)
