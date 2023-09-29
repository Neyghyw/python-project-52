from task_manager.users.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from task_manager.labels.models import Label
from task_manager.statuses.models import Status


# Create your models here.
class Task(models.Model):
    name = models.CharField(max_length=255,
                            unique=True,
                            verbose_name=_('Name'))

    description = models.TextField(verbose_name=_('Description'))

    status = models.ForeignKey(Status,
                               on_delete=models.PROTECT,
                               related_name='status',
                               verbose_name=_('Status'))

    labels = models.ManyToManyField(Label,
                                    blank=True,
                                    related_name='labels',
                                    verbose_name=_('Label'))

    creator = models.ForeignKey(User,
                                related_name='task_creator',
                                on_delete=models.PROTECT,
                                blank=False,
                                verbose_name=_('Creator'))

    executor = models.ForeignKey(User,
                                 related_name='task_executor',
                                 on_delete=models.PROTECT,
                                 verbose_name=_('Executor'))

    created_at = models.DateField(auto_now_add=True, verbose_name=_('Created at'))

    def __str__(self):
        return self.name
