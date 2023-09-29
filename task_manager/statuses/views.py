from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models.deletion import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django.utils.translation import gettext_lazy as _

from statuses.models import Status


class StatusListView(ListView, LoginRequiredMixin):
    model = Status
    template_name = 'statuses/statuses.html'
    context_object_name = 'statuses'


class StatusCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    template_name = 'statuses/status_create.html'
    model = Status
    fields = ["name"]
    success_url = reverse_lazy('statuses_list')
    success_message = _("Success! New status was created.")


class StatusDeleteView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = Status
    template_name = 'statuses/status_delete.html'
    success_url = reverse_lazy('statuses_list')
    success_message = _("Success! Chosen status was deleted.")

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            error_text = _("Operation isn't possible."
                           " This status linked with exist task.")
            messages.add_message(request, messages.ERROR, error_text)
            return redirect(self.success_url)


class StatusUpdateView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = Status
    template_name = 'statuses/status_update.html'
    fields = ["name"]
    success_url = reverse_lazy('statuses_list')
    success_message = _("Success! Status was updated.")
