from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from task_manager.mixins import RelatedObjectAccessMixin
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task


class StatusAccessMixin(LoginRequiredMixin, RelatedObjectAccessMixin):

    def dispatch(self, request, *args, **kwargs):
        status = Status.objects.get(id=kwargs.get('pk'))
        self.related_model = Task
        self.dispatch_constraint = Q(status=status)
        return super().dispatch(request, *args, **kwargs)
