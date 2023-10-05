from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from task_manager.users.forms import UserForm
from task_manager.users.mixins import UserAccessMixin
from task_manager.users.models import User


class UserListView(ListView):
    model = User
    template_name = 'users/users.html'
    context_object_name = 'users'


class UserCreateView(SuccessMessageMixin, CreateView):
    template_name = 'users/create.html'
    form_class = UserForm
    success_url = reverse_lazy('login_user')
    success_message = _('Success! User was created.')


class UserUpdateView(UserAccessMixin,
                     UpdateView):
    model = User
    template_name = 'users/update.html'
    form_class = UserForm
    success_url = reverse_lazy('users_list')
    success_message = _('Success! User was updated.')


class UserDeleteView(UserAccessMixin,
                     DeleteView):
    model = User
    success_url = reverse_lazy('users_list')
    success_message = _('Success! Chosen user was deleted.')
    template_name = 'delete.html'
