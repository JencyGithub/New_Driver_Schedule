# Generated by Django 4.2.1 on 2023-12-28 03:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account_app', '0020_alter_driverdocket_shiftdate_alter_rcti_unit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driverdocket',
            name='shiftDate',
            field=models.DateField(default=datetime.datetime(2023, 12, 28, 3, 59, 13, 586472, tzinfo=datetime.timezone.utc), null=True),
        ),
    ]
