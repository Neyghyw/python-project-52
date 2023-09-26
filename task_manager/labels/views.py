from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from tasks.models import Task
from labels.models import Label
from django.shortcuts import redirect
from django.contrib import messages


class LabelsListView(ListView):
    model = Label
    template_name = 'labels/labels.html'
    context_object_name = 'labels'


class LabelsCreateView(SuccessMessageMixin,
                       LoginRequiredMixin,
                       CreateView):
    template_name = 'labels/label_create.html'
    model = Label
    fields = ['name']
    success_url = reverse_lazy('labels_list')
    success_message = "Success! New label was created."


class LabelsDeleteView(SuccessMessageMixin,
                       LoginRequiredMixin,
                       DeleteView):
    model = Label
    template_name = 'labels/label_delete.html'
    success_url = reverse_lazy('labels_list')
    success_message = "Success! Chosen label was deleted."

    def post(self, request, *args, **kwargs):
        label = Label.objects.get(id=kwargs['pk'])
        tasks = Task.objects.filter(label=label)
        if tasks:
            error_text = ("Operation isn't possible."
                          " This label linked with exist task.")
            messages.add_message(request, messages.ERROR, error_text)
            return redirect(self.success_url)
        return super().post(request, *args, **kwargs)


class LabelsUpdateView(SuccessMessageMixin,
                       LoginRequiredMixin,
                       UpdateView):
    model = Label
    fields = ['name']
    template_name = 'labels/label_update.html'
    success_url = reverse_lazy('labels_list')
    success_message = "Success! Label was updated."
