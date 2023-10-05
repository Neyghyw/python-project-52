from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django_filters.views import FilterView

from task_manager.tasks.filters import TaskFilter
from task_manager.tasks.mixins import TaskAccessMixin
from task_manager.tasks.models import Task


class TasksListView(FilterView, LoginRequiredMixin):
    model = Task
    filterset_class = TaskFilter
    template_name = 'tasks/tasks.html'
    context_object_name = 'tasks'


class TaskDetailView(DetailView, LoginRequiredMixin):
    model = Task
    template_name = 'tasks/task.html'
    context_object_name = 'task'


class TasksCreateView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    template_name = 'tasks/create.html'
    model = Task
    fields = ['name', 'description', 'status', 'labels', 'executor']
    success_url = reverse_lazy('tasks_list')
    success_message = _('Success! New task was created.')

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class TasksUpdateView(LoginRequiredMixin,
                      TaskAccessMixin,
                      SuccessMessageMixin,
                      UpdateView):
    model = Task
    fields = ['name', 'description', 'status', 'labels', 'executor']
    template_name = 'tasks/update.html'
    success_url = reverse_lazy('tasks_list')
    success_message = _('Success! Task was updated.')


class TasksDeleteView(LoginRequiredMixin,
                      TaskAccessMixin,
                      SuccessMessageMixin,
                      DeleteView):
    model = Task
    template_name = 'delete.html'
    success_url = reverse_lazy('tasks_list')
    success_message = _('Success! Chosen task was deleted.')

    def post(self, request, *args, **kwargs):
        messages.success(request, self.success_message)
        return self.delete(request, *args, **kwargs)
