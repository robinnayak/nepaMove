# Generated by Django 5.0 on 2024-03-22 12:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Driver', '0004_alter_driver_date_of_birth'),
        ('passenger', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vehicle',
            old_name='make',
            new_name='company_made',
        ),
        migrations.AddField(
            model_name='vehicle',
            name='available_seat',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='driver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Driver.driver'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='seating_capacity',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_passenger', models.PositiveBigIntegerField(default=1)),
                ('is_paid', models.BooleanField(default=False)),
                ('booking_date', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='passenger.passenger')),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Driver.vehicle')),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticket_file', models.FileField(upload_to='tickets/')),
                ('num_passenger', models.PositiveIntegerField(default=0)),
                ('booking', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Driver.booking')),
                ('passenger', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='passenger.passenger')),
            ],
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_datetime', models.DateTimeField(blank=True, null=True)),
                ('end_datetime', models.DateTimeField(blank=True, null=True)),
                ('end_location', models.CharField(max_length=255)),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='driver_trips', to='Driver.driver')),
                ('passenger', models.ManyToManyField(blank=True, related_name='passenger_trips', to='passenger.passenger')),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vehicle_trips', to='Driver.vehicle')),
            ],
        ),
    ]
