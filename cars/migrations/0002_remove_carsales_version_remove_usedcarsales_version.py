# Generated by Django 5.0 on 2023-12-22 06:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='carsales',
            name='version',
        ),
        migrations.RemoveField(
            model_name='usedcarsales',
            name='version',
        ),
    ]
