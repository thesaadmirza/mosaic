# Generated by Django 3.0.7 on 2020-07-07 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0003_auto_20200705_1401'),
        ('booking', '0002_remove_booking_access_arrangments'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='service',
        ),
        migrations.AddField(
            model_name='booking',
            name='service',
            field=models.ManyToManyField(related_name='bookings', to='services.Service'),
        ),
    ]
