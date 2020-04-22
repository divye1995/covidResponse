# Generated by Django 3.0.2 on 2020-04-21 16:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_auto_20200421_1559'),
        ('baseapp', '0051_entity_region'),
    ]

    operations = [
        migrations.AddField(
            model_name='entity',
            name='assigned_to_group',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='org_group', to='core.Group'),
        ),
    ]