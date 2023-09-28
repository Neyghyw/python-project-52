from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from tasks.filters import TaskFilter
from tasks.models import Task
from tasks.utils import TaskAccessMixin
from django_filters.views import FilterView


class TasksListView(FilterView):
    model = Task
    filterset_class = TaskFilter
    template_name = 'tasks/tasks.html'
    context_object_name = 'tasks'


class TasksCreateView(SuccessMessageMixin,
                      LoginRequiredMixin,
                      CreateView):
    template_name = 'tasks/task_create.html'
    model = Task
    fields = ['name', 'description', 'status', 'label', 'executor']
    success_url = reverse_lazy('tasks_list')
    success_message = "Success! New task was created."

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class TasksDeleteView(SuccessMessageMixin,
                      LoginRequiredMixin,
                      TaskAccessMixin,
                      DeleteView):
    model = Task
    template_name = 'tasks/task_delete.html'
    success_url = reverse_lazy('tasks_list')
    success_message = "Success! Chosen task was deleted."


class TasksUpdateView(SuccessMessageMixin,
                      LoginRequiredMixin,
                      TaskAccessMixin,
                      UpdateView):
    model = Task
    fields = ['name', 'description', 'status', 'executor']
    template_name = 'tasks/task_update.html'
    success_url = reverse_lazy('tasks_list')
    success_message = "Success! Task was updated."
