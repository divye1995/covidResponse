# Generated by Django 3.0.2 on 2020-05-03 17:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_user_wasan_username'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='wasan_username',
            new_name='wassan_username',
        ),
    ]
