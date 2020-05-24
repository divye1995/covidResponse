# Generated by Django 3.0.2 on 2020-05-24 00:22

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_auto_20200520_0817'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2020, 5, 24, 0, 22, 23, 886677, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='organization',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]