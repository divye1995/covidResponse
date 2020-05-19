# Generated by Django 3.0.2 on 2020-05-19 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_auto_20200518_1906'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='endorsed_by',
            field=models.CharField(blank=True, max_length=4096, null=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='total_endorsed',
            field=models.BigIntegerField(blank=True, default=0, null=True),
        ),
    ]
