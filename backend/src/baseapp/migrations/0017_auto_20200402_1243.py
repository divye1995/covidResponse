# Generated by Django 3.0.2 on 2020-04-02 12:43

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('baseapp', '0016_context_is_facility'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Context',
            new_name='Entity',
        ),
    ]
