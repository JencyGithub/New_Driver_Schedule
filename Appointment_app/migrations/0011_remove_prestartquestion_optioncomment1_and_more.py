# Generated by Django 4.2.2 on 2024-01-13 10:47

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Appointment_app', '0010_remove_prestart_comment_remove_prestart_curdate_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='prestartquestion',
            name='optionComment1',
        ),
        migrations.RemoveField(
            model_name='prestartquestion',
            name='optionComment2',
        ),
        migrations.RemoveField(
            model_name='prestartquestion',
            name='optionComment3',
        ),
        migrations.RemoveField(
            model_name='prestartquestion',
            name='optionComment4',
        ),
        migrations.RemoveField(
            model_name='prestartquestion',
            name='optionFile1',
        ),
        migrations.RemoveField(
            model_name='prestartquestion',
            name='optionFile2',
        ),
        migrations.RemoveField(
            model_name='prestartquestion',
            name='optionFile3',
        ),
        migrations.RemoveField(
            model_name='prestartquestion',
            name='optionFile4',
        ),
        migrations.AlterField(
            model_name='appointment',
            name='Created_time',
            field=models.TimeField(default=datetime.datetime(2024, 1, 13, 10, 47, 7, 73622, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='End_Date_Time',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 13, 10, 47, 7, 73622, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='Start_Date_Time',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 13, 10, 47, 7, 73622, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='report_to_origin',
            field=models.DateTimeField(default=datetime.datetime(2024, 1, 13, 10, 47, 7, 73622, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='prestartquestion',
            name='questionType',
            field=models.CharField(choices=[('Vehicle related', 'Vehicle related'), ('Driver related', 'Driver related'), ('Other', 'Other')], max_length=20),
        ),
    ]
