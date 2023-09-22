from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models.deletion import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from statuses.forms import StatusForm
from statuses.models import Status


class StatusListView(ListView):
    model = Status
    template_name = 'statuses/statuses.html'
    context_object_name = 'statuses'


class StatusCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    template_name = 'statuses/status_create.html'
    form_class = StatusForm
    success_url = reverse_lazy('statuses_list')
    success_message = "Success! New status was created."


class StatusDeleteView(SuccessMessageMixin, LoginRequiredMixin,  DeleteView):
    model = Status
    template_name = 'statuses/status_delete.html'
    success_url = reverse_lazy('statuses_list')
    success_message = "Success! Chosen status was deleted."

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            error_text = ("Operation isn't possible."
                          " This status linked with exist task.")
            messages.add_message(request, messages.ERROR, error_text)
            return redirect(self.success_url)


class StatusUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Status
    template_name = 'statuses/status_update.html'
    form_class = StatusForm
    success_url = reverse_lazy('statuses_list')
    success_message = "Success! Status was updated."
