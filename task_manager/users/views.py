from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render, reverse
from users.forms import LoginForm, RegisterForm, UpdateForm


def index(request):
    users = User.objects.all()
    return render(request, 'users.html', {'users': users})


def create(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    form = RegisterForm(request.POST)
    if not form.is_valid():
        messages.error(request, f"Please, fill register-form fields without errors.")
        return redirect(reverse('create'))
    if authenticate(request, **form.cleaned_data):
        messages.error(request, f"User {form.cleaned_data['username']} already exist.")
        return redirect(reverse('create'))
    user = User.objects.create_user(**form.cleaned_data)
    messages.info(request, f"User {user.username} create.")
    return redirect(reverse('main'))


def delete(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user.delete()
    messages.info(request, f"User {user.username} delete.")
    return redirect(reverse('users_list'))


def update(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    if request.method == 'GET':
        return render(request, 'update_user.html', {'user': user})
    if request.method == 'POST':
        form = UpdateForm(request.POST, instance=user)
        if not form.is_valid():
            messages.error(request, f"Please, fill form fields without errors.")
            return render(request, 'update_user.html', {'user': user, 'form_errors': form.errors})
        if form.cleaned_data['password'] == form.cleaned_data['confirm_password']:
            form.save()
            messages.info(request, f"User with id {user.id} update.")
        else:
            messages.error(request, f"Passwords doesn't equal.")
            return render(request, 'update_user.html', {'user': user, 'form_errors': form.errors})
    return redirect(reverse('users_list'))


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
