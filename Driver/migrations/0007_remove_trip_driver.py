# Generated by Django 5.0 on 2024-03-23 02:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Driver', '0006_rename_year_vehicle_age'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trip',
            name='driver',
        ),
    ]
