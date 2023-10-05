from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from task_manager.labels.models import Label
from task_manager.tasks.models import Task


class LabelsListView(ListView, LoginRequiredMixin):
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


class LabelsDeleteView(LoginRequiredMixin, DeleteView):
    model = Label
    template_name = 'delete.html'
    success_url = reverse_lazy('labels_list')
    success_message = _('Success! Chosen label was deleted.')

    def post(self, request, *args, **kwargs):
        label = self.get_object()
        tasks = Task.objects.filter(labels=label)
        if tasks:
            error_text = _("Operation isn't possible."
                           " This label linked with exist task.")
            messages.add_message(request, messages.ERROR, error_text)
            return redirect(self.success_url)
        messages.add_message(request, messages.INFO, self.success_message)
        return super().post(request, *args, **kwargs)
