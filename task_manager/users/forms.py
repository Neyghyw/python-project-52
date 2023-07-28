from django.forms.fields import CharField
from django.forms.forms import Form


class LoginForm(Form):
    username = CharField(min_length=3, max_length=150, label='username')
    password = CharField(min_length=3, max_length=150, label='password')
