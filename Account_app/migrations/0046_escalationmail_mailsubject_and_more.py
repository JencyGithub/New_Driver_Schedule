# Generated by Django 4.2.1 on 2024-01-07 16:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account_app', '0045_escalation_docketdate_alter_driverdocket_shiftdate'),
    ]

    operations = [
        migrations.AddField(
            model_name='escalationmail',
            name='mailSubject',
            field=models.CharField(default=None, max_length=255),
        ),
        migrations.AlterField(
            model_name='driverdocket',
            name='shiftDate',
            field=models.DateField(default=datetime.datetime(2024, 1, 7, 16, 17, 45, 768163, tzinfo=datetime.timezone.utc), null=True),
        ),
    ]
