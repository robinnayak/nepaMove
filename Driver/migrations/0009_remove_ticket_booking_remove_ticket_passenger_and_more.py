# Generated by Django 5.0 on 2024-03-26 03:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Driver', '0008_trip_start_location_alter_trip_end_location'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='booking',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='passenger',
        ),
        migrations.RemoveField(
            model_name='trip',
            name='passenger',
        ),
        migrations.RemoveField(
            model_name='trip',
            name='vehicle',
        ),
        migrations.DeleteModel(
            name='Booking',
        ),
        migrations.DeleteModel(
            name='Ticket',
        ),
        migrations.DeleteModel(
            name='Trip',
        ),
    ]
