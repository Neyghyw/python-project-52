from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from task_manager.labels.mixins import LabelAccessMixin
from task_manager.labels.models import Label


class LabelsListView(LoginRequiredMixin, ListView):
    model = Label
    template_name = 'labels/labels.html'
    context_object_name = 'labels'


class LabelsCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    template_name = 'labels/create.html'
    model = Label
    fields = ['name']
    success_url = reverse_lazy('labels_list')
    success_message = _("Success! New label was created.")


class LabelsUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Label
    fields = ['name']
    template_name = 'labels/update.html'
    success_url = reverse_lazy('labels_list')
    success_message = _('Success! Label was updated.')


class LabelsDeleteView(LabelAccessMixin, LoginRequiredMixin, DeleteView):
    model = Label
    template_name = 'delete.html'
    success_url = reverse_lazy('labels_list')
    success_message = _('Success! Chosen label was deleted.')
