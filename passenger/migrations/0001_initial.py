# Generated by Django 5.0 on 2024-01-03 15:09

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Passenger',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(blank=True, max_length=15)),
                ('address', models.CharField(blank=True, max_length=255)),
                ('emergency_contact_name', models.CharField(blank=True, max_length=50)),
                ('emergency_contact_number', models.CharField(blank=True, max_length=10)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('preferred_language', models.CharField(blank=True, choices=[('en', 'English'), ('ne', 'Nepali')], max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_query_name='user_passenger', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
