from django.db import models


# Create your models here.
class Status(models.Model):
    name = models.CharField(max_length=255,
                            unique=True,
                            verbose_name='Name')

    description = models.CharField(max_length=255,
                                   verbose_name='Description')

    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name
