from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models.deletion import ProtectedError
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from users.forms import UserForm

from .mixins import UserAccessMixin


class UserLoginView(LoginView):
    template_name = 'users/signin.html'
    next_page = reverse_lazy('main')


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('login_user')


class UserListView(ListView):
    model = User
    template_name = 'users/users.html'
    context_object_name = 'users'


class UserCreateView(SuccessMessageMixin,
                     CreateView):
    template_name = 'users/signup.html'
    form_class = UserForm
    success_url = reverse_lazy('login_user')
    success_message = _("Success! User was created.")


class UserDeleteView(SuccessMessageMixin,
                     UserAccessMixin,
                     DeleteView):
    model = User
    success_url = reverse_lazy('users_list')
    success_message = _("Success! Chosen user was deleted.")
    template_name = 'users/delete.html'

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            error_text = _("Operation isn't possible."
                           " This user linked with exist task.")
            messages.add_message(request, messages.ERROR, error_text)
            return redirect(self.success_url)


class UserUpdateView(SuccessMessageMixin,
                     UserAccessMixin,
                     UpdateView):
    model = User
    template_name = 'users/update_user.html'
    form_class = UserForm
    success_url = reverse_lazy('users_list')
    success_message = _("Success! User was updated.")
