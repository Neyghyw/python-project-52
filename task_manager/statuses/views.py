from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from task_manager.statuses.mixins import StatusAccessMixin
from task_manager.statuses.models import Status


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


class StatusDeleteView(StatusAccessMixin, LoginRequiredMixin, DeleteView):
    model = Status
    template_name = 'delete.html'
    success_url = reverse_lazy('statuses_list')
    success_message = _('Success! Chosen status was deleted.')
