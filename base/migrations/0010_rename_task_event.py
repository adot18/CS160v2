# Generated by Django 4.0.2 on 2022-05-17 02:54

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('base', '0009_alter_task_ring'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Task',
            new_name='Event',
        ),
    ]