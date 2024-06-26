# Generated by Django 5.0 on 2024-03-31 03:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Driver', '0020_remove_ticket_booking_delete_booking_delete_ticket'),
        ('passenger', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('booking_id', models.CharField(default='passenger2JANKATXYZ1234', max_length=200, unique=True)),
                ('num_passengers', models.PositiveIntegerField()),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('passenger', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='passenger.passenger')),
                ('tripprice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Driver.tripprice')),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticket_file', models.FileField(upload_to='tickets/')),
                ('booking', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Driver.booking')),
            ],
        ),
    ]
