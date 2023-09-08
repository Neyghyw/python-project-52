from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from users.forms import UserForm

from .utils import UserAccessMixin


class UserLoginView(LoginView):
    template_name = 'signin.html'
    next_page = reverse_lazy('main')


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('login_user')


class UserListView(ListView):
    model = User
    template_name = 'users.html'
    context_object_name = 'users'


class UserCreateView(SuccessMessageMixin,
                     CreateView):
    template_name = 'signup.html'
    form_class = UserForm
    success_url = reverse_lazy('login_user')
    success_message = "Success! User with username %(username)s was created."


class UserDeleteView(SuccessMessageMixin,
                     UserAccessMixin,
                     DeleteView):
    model = User
    success_url = reverse_lazy('users_list')
    success_message = "Success! Chosen user was deleted."
    template_name = 'delete.html'


class UserUpdateView(SuccessMessageMixin,
                     UserAccessMixin,
                     UpdateView):
    model = User
    template_name = 'update_user.html'
    form_class = UserForm
    success_url = reverse_lazy('users_list')
    success_message = "Success! User was updated."
