# Generated by Django 3.2.21 on 2023-10-03 06:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('statuses', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='status',
            name='created_at',
            field=models.DateField(auto_now_add=True, verbose_name='Created at'),
        ),
    ]
