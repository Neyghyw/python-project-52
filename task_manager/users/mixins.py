from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from task_manager.mixins import RelatedObjectAccessMixin
from task_manager.tasks.models import Task


class UserAccessMixin(LoginRequiredMixin, RelatedObjectAccessMixin):

    def dispatch(self, request, *args, **kwargs):
        if kwargs.get('pk') != request.user.id:
            messages.error(request, _('Access granted'
                                      ' only for authorized owner.'))
            return redirect(reverse_lazy('users_list'))

        user = request.user
        self.related_model = Task
        self.dispatch_constraint = Q(creator=user) | Q(executor=user)
        return super().dispatch(request, *args, **kwargs)
