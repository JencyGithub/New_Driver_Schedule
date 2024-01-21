# Generated by Django 4.2.1 on 2024-01-20 20:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account_app', '0073_drivershiftdocket_shiftid_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='drivershiftdocket',
            name='clientId',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='driverdocket',
            name='shiftDate',
            field=models.DateField(default=datetime.datetime(2024, 1, 20, 20, 36, 37, 283124, tzinfo=datetime.timezone.utc), null=True),
        ),
    ]
