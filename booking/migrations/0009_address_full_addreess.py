# Generated by Django 3.0.7 on 2020-07-14 07:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0008_businesshours'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='full_addreess',
            field=models.CharField(default=1, max_length=250, verbose_name='Full Address'),
            preserve_default=False,
        ),
    ]
