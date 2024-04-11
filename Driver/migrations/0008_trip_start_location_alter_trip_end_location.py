# Generated by Django 5.0 on 2024-03-25 01:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Driver', '0007_remove_trip_driver'),
    ]

    operations = [
        migrations.AddField(
            model_name='trip',
            name='start_location',
            field=models.CharField(default='janakpur', max_length=255),
        ),
        migrations.AlterField(
            model_name='trip',
            name='end_location',
            field=models.CharField(default='kathmandu', max_length=255),
        ),
    ]
