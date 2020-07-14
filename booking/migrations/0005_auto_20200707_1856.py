# Generated by Django 3.0.7 on 2020-07-07 13:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_staff'),
        ('booking', '0004_auto_20200707_1848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='staff',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='users.Staff'),
        ),
    ]