from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from task_manager.tasks.models import Task
from task_manager.users.forms import UserForm
from task_manager.users.models import User

from .mixins import UserAccessMixin


class UserListView(ListView):
    model = User
    template_name = 'users/users.html'
    context_object_name = 'users'


class UserCreateView(SuccessMessageMixin, CreateView):
    template_name = 'users/create.html'
    form_class = UserForm
    success_url = reverse_lazy('login_user')
    success_message = _('Success! User was created.')


class UserUpdateView(SuccessMessageMixin,
                     UserAccessMixin,
                     UpdateView):
    model = User
    template_name = 'users/update.html'
    form_class = UserForm
    success_url = reverse_lazy('users_list')
    success_message = _('Success! User was updated.')


class UserDeleteView(UserAccessMixin, DeleteView):
    model = User
    success_url = reverse_lazy('users_list')
    success_message = _('Success! Chosen user was deleted.')
    template_name = 'delete.html'

    def post(self, request, *args, **kwargs):
        user = self.get_object()
        filter_expression = Q(creator=user) | Q(executor=user)
        referenced_tasks = Task.objects.filter(filter_expression)

        if not referenced_tasks:
            messages.info(request, self.success_message)
            return super().post(request, *args, **kwargs)

        error_text = _('This user linked with exist task.')
        messages.error(request, error_text)
        return redirect(self.success_url)
