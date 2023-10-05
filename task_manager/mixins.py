from django.contrib import messages
from django.contrib.auth.mixins import AccessMixin
from django.db.models import Model, Q
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _


class RelatedObjectAccessMixin(AccessMixin):
    """
    Mixin to handle an action on a related object
    """
    dispatch_constraint: Q
    related_model: Model
    success_url: str

    def dispatch(self, request, *args, **kwargs):
        filter_results = self.related_model.objects.filter(self.dispatch_constraint)
        if filter_results.first():
            messages.error(self.request, _('Sorry,'
                                           ' This object related with another table.'
                                           ' Permission denied.'))
            return redirect(self.success_url)
        messages.success(self.request, self.success_message)
        return super().dispatch(request, *args, **kwargs)
