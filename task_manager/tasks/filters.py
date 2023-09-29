import django_filters
from django.contrib.auth.models import User
from django.forms import CheckboxInput, SelectMultiple
from django.utils.translation import gettext_lazy as _

from labels.models import Label
from statuses.models import Status
from tasks.models import Task


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(queryset=Status.objects.all(),
                                              label=_("status"),
                                              localize=True)

    executor = django_filters.ModelChoiceFilter(queryset=User.objects.all(),
                                                label=_("executor"),
                                                localize=True)

    label = django_filters.ModelMultipleChoiceFilter(queryset=Label.objects.all(),  # noqa: E501
                                                     widget=SelectMultiple,
                                                     label=_("label"),
                                                     localize=True)

    self_tasks = django_filters.BooleanFilter(field_name='creator',
                                              label=_('only my tasks'),
                                              localize=True,
                                              method='self_tasks_filter',
                                              widget=CheckboxInput)

    def self_tasks_filter(self, queryset, name, value):
        current_user = self.request.user.id
        if value is True:
            return queryset.filter(creator=current_user)
        return queryset

    class Meta:
        model = Task
        fields = ['status', 'executor', 'label', 'self_tasks']
