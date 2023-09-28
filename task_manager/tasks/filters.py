import django_filters
from tasks.models import Task
from statuses.models import Status
from labels.models import Label
from django.forms import CheckboxInput, SelectMultiple
from django.contrib.auth.models import User


class TaskFilter(django_filters.FilterSet):
    status = django_filters.ModelChoiceFilter(queryset=Status.objects.all())
    executor = django_filters.ModelChoiceFilter(queryset=User.objects.all())
    label = django_filters.ModelMultipleChoiceFilter(queryset=Label.objects.all(),  # noqa: E501
                                                     widget=SelectMultiple)
    self_tasks = django_filters.BooleanFilter(field_name='creator',
                                              label='only my tasks',
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

# по статусу, исполнителю и наличию метки
# отображать задачи, автором которых он является
