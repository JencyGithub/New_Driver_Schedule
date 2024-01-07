# Generated by Django 4.2.1 on 2023-12-14 10:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Appointment_app', '0003_alter_appointment_created_by_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='shiftType',
            field=models.CharField(choices=[('Day', 'Day'), ('Night', 'Night')], default='Day', max_length=10),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='Created_time',
            field=models.TimeField(default=datetime.datetime(2023, 12, 14, 10, 49, 49, 816052, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='End_Date_Time',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 14, 10, 49, 49, 816052, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='Start_Date_Time',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 14, 10, 49, 49, 816052, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='report_to_origin',
            field=models.DateTimeField(default=datetime.datetime(2023, 12, 14, 10, 49, 49, 816052, tzinfo=datetime.timezone.utc)),
        ),
    ]