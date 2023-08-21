from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render, reverse
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from users.forms import LoginForm, UserRegisterForm, UserUpdateForm
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.base import ContextMixin

class UserListView(ListView):
    template_name = 'users.html'
    context_object_name = 'users'
    model = User


class UserCreateView(SuccessMessageMixin, CreateView):
    template_name = 'signup.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('login_user')
    success_message = "Success! User with username %(username)s was created."

    def form_invalid(self, form):
        if form.has_error(field='username', code='unique'):
            messages.error(self.request, f"Sorry. User with given username already exist.")
        else:
            messages.error(self.request, f"Please, fill register-form fields without errors.")
            messages.error(self.request, form.errors)
        return redirect(reverse_lazy('create_user'))


class UserDeleteView(SuccessMessageMixin, DeleteView):
    model = User
    success_url = reverse_lazy('users_list')
    success_message = "Success! Chosen user was deleted."
    template_name = 'delete.html'


class UserUpdateView(SuccessMessageMixin, UpdateView):
    model = User
    template_name = 'update_user.html'
    form_class = UserUpdateForm
    success_url = reverse_lazy('users_list')
    success_message = "Success! User was updated."

    def form_invalid(self, form):
        messages.error(self.request, f"Please, fill form fields without errors.")
        messages.error(self.request, form.errors)
        return redirect(reverse_lazy('update_user', kwargs={'pk': form.instance.id}))


def login_user(request):
    if request.method == 'GET':
        return render(request, 'signin.html')
    form = LoginForm(request.POST)
    if not form.is_valid():
        messages.error(request, f"Please, fill form fields without errors.")
        return redirect(reverse('login_user'))
    user = authenticate(request, **form.cleaned_data)
    if user is not None:
        login(request, user)
    else:
        messages.error(request, "Login error. Please, check login credentials and try again.")
        return redirect(reverse('login_user'))
    messages.success(request, f"User \"{user.username}\" login in system.")
    return redirect(reverse('main'))


def logout_user(request):
    logout(request)
    return redirect(reverse('login_user'))
