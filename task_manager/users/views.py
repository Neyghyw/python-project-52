from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render, reverse

from users.forms import LoginForm


def index(request):
    return render(request, 'users.html')


def create(request):
    user = User.objects.create_user("john", "lennon@thebeatles.com", "johnpassword")
    messages.info(request, f"User {user.username} create.")
    return redirect(reverse('users'))


def delete(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.delete()
    messages.info(request, f"User {user.username} delete.")
    return redirect(reverse('users'))


def update(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    messages.info(request, f"User {user.username} update.")
    return redirect(reverse('users'))


def login_user(request):
    form = LoginForm(request.POST)
    if not form.is_valid():
        messages.error(request, f"Please, fill form fields without errors.")
        return redirect(reverse('signin'))
    user = authenticate(request, **form.cleaned_data)
    if user is not None:
        login(request, user)
    else:
        messages.error(request, "User not found. Please, check login credentials and try again.")
        return redirect(reverse('signin'))
    messages.success(request, f"User \"{user.username}\" login in system.")
    return redirect(reverse('users_list'))


def logout_user(request):
    logout(request)
    return redirect(reverse('signin'))
