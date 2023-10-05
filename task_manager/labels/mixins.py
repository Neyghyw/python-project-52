from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from task_manager.labels.models import Label
from task_manager.mixins import RelatedObjectAccessMixin
from task_manager.tasks.models import Task


class LabelAccessMixin(LoginRequiredMixin, RelatedObjectAccessMixin):

    def dispatch(self, request, *args, **kwargs):
        label = Label.objects.get(id=kwargs.get('pk'))
        self.related_model = Task
        self.dispatch_constraint = Q(labels=label)
        return super().dispatch(request, *args, **kwargs)
