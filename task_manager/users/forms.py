from django.forms.fields import CharField
from django.forms.forms import Form
from django.forms import ModelForm
from django.contrib.auth.models import User


class LoginForm(Form):
    username = CharField(min_length=3, max_length=150, label='username')
    password = CharField(min_length=3, max_length=150, label='password')


class RegisterForm(Form):
    first_name = CharField(min_length=3, max_length=150, label='first_name')
    last_name = CharField(min_length=3, max_length=150, label='last_name')
    username = CharField(min_length=3, max_length=150, label='username')
    password = CharField(min_length=3, max_length=150, label='password')


class UpdateForm(ModelForm):
    confirm_password = CharField(required=False, min_length=3, max_length=150, label='confirm_password')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 'confirm_password']
