from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from labels.models import Label
from statuses.models import Status


# Create your models here.
class Task(models.Model):
    name = models.CharField(max_length=255,
                            unique=True,
                            verbose_name=_('Name'))

    description = models.CharField(max_length=255,
                                   verbose_name=_('Description'))

    status = models.ForeignKey(Status,
                               on_delete=models.PROTECT,
                               related_name='status',
                               verbose_name=_('Status'))

    label = models.ManyToManyField(Label,
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
