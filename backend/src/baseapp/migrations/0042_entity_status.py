# Generated by Django 3.0.2 on 2020-04-19 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baseapp', '0041_bulkoperation_ids_json'),
    ]

    operations = [
        migrations.AddField(
            model_name='entity',
            name='status',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]
