# Generated by Django 4.2.1 on 2023-12-14 04:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account_app', '0009_alter_driverdocket_shiftdate_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='holcimdocket',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='holcimdocket',
            name='ticketedDate',
            field=models.DateField(default=None, null=True),
        ),
        migrations.AddField(
            model_name='holcimdocket',
            name='ticketedTime',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='driverdocket',
            name='shiftDate',
            field=models.DateField(default=datetime.datetime(2023, 12, 14, 4, 46, 30, 480610, tzinfo=datetime.timezone.utc), null=True),
        ),
        migrations.AlterUniqueTogether(
            name='holcimdocket',
            unique_together={('jobNo', 'ticketedDate', 'truckNo')},
        ),
        migrations.RemoveField(
            model_name='holcimdocket',
            name='ticketed',
        ),
    ]