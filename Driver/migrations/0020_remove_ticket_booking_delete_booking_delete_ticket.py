# Generated by Django 5.0 on 2024-03-31 03:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Driver', '0019_alter_tripprice_trip_price_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='booking',
        ),
        migrations.DeleteModel(
            name='Booking',
        ),
        migrations.DeleteModel(
            name='Ticket',
        ),
    ]
