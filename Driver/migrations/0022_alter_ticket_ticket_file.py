# Generated by Django 5.0 on 2024-03-31 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Driver', '0021_booking_ticket'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='ticket_file',
            field=models.FileField(upload_to=''),
        ),
    ]
