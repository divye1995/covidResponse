# Generated by Django 3.0.2 on 2020-05-07 08:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baseapp', '0061_entityhistory_modified'),
    ]

    operations = [
        migrations.AddField(
            model_name='entity',
            name='district',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
    ]