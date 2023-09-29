from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.translation import gettext_lazy as _


class IndexView(TemplateView, LoginRequiredMixin):
    template_name = 'index.html'


class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = 'users/signin.html'
    next_page = reverse_lazy('main')
    success_message = _("Success! You were logged.")


class UserLogoutView(SuccessMessageMixin, LogoutView):
    next_page = reverse_lazy('main')

    def dispatch(self, request, *args, **kwargs):
        response = super().dispatch(request, *args, **kwargs)
        messages.add_message(request, messages.INFO, _("Success! You are not logged."))
        return response
