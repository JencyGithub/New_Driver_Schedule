# Generated by Django 4.2.1 on 2024-01-04 12:33

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account_app', '0030_rctiexpense_rctireport_alter_driverdocket_shiftdate'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rctiexpense',
            name='rctiReport',
        ),
        migrations.AlterField(
            model_name='driverdocket',
            name='shiftDate',
            field=models.DateField(default=datetime.datetime(2024, 1, 4, 12, 33, 22, 508060, tzinfo=datetime.timezone.utc), null=True),
        ),
    ]