# Generated by Django 4.2.1 on 2024-01-19 17:35

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account_app', '0068_alter_driverdocket_shiftdate_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driverdocket',
            name='shiftDate',
            field=models.DateField(default=datetime.datetime(2024, 1, 19, 17, 35, 6, 599746, tzinfo=datetime.timezone.utc), null=True),
        ),
    ]
