# Generated by Django 5.0 on 2024-01-06 07:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Driver', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driver',
            name='driving_experience',
            field=models.IntegerField(default=1),
        ),
    ]