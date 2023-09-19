from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy

from tasks.models import Task


class TaskAccessMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        user_id = request.user
        task_id = kwargs.get('pk')
        task = Task.objects.get(id=task_id)
        task_creator = task.creator
        if task_creator != user_id:
            message_text = 'Access granted only for owner.'
            messages.add_message(request, messages.ERROR, message_text)
            return redirect(reverse_lazy('tasks_list'))
        return super().dispatch(request, *args, **kwargs)
