# Generated by Django 3.0.2 on 2020-04-23 04:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20200423_0255'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.CharField(default='native', max_length=32),
        ),
    ]
