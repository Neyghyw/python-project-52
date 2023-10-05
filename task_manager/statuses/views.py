from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from task_manager.statuses.models import Status
from task_manager.tasks.models import Task


class StatusListView(ListView, LoginRequiredMixin):
    model = Status
    template_name = 'statuses/statuses.html'
    context_object_name = 'statuses'


class StatusCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    template_name = 'statuses/create.html'
    model = Status
    fields = ['name']
    success_url = reverse_lazy('statuses_list')
    success_message = _('Success! New status was created.')


class StatusUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Status
    template_name = 'statuses/update.html'
    fields = ['name']
    success_url = reverse_lazy('statuses_list')
    success_message = _('Success! Status was updated.')


class StatusDeleteView(LoginRequiredMixin, DeleteView):
    model = Status
    template_name = 'delete.html'
    success_url = reverse_lazy('statuses_list')
    success_message = _('Success! Chosen status was deleted.')

    def post(self, request, *args, **kwargs):
        status = self.get_object()
        referenced_tasks = Task.objects.filter(status=status)
        if not referenced_tasks:
            messages.add_message(request, messages.INFO, self.success_message)
            return super().post(request, *args, **kwargs)
        error_text = _("Operation isn't possible."
                       " This status linked with exist task.")
        messages.add_message(request, messages.ERROR, error_text)
        return redirect(self.success_url)
