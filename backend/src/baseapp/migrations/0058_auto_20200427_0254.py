# Generated by Django 3.0.2 on 2020-04-27 02:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baseapp', '0057_auto_20200427_0243'),
    ]

    operations = [
        migrations.RenameField(
            model_name='entityhistory',
            old_name='data_json',
            new_name='prefill_json',
        ),
        migrations.AddField(
            model_name='entityhistory',
            name='title',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
