# Generated by Django 5.0.1 on 2024-02-21 06:59

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GearBox_app', '0018_admintruck_trucksetting_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clienttruckconnection',
            name='clientOfc',
        ),
        migrations.RemoveField(
            model_name='clienttruckconnection',
            name='neverEnding',
        ),
        migrations.AlterField(
            model_name='clienttruckconnection',
            name='startDate',
            field=models.DateField(default=datetime.datetime(2024, 2, 21, 6, 59, 48, 306640, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='costparameters',
            name='end_date',
            field=models.DateField(blank=True, default=datetime.datetime(2034, 2, 18, 6, 59, 48, 291015, tzinfo=datetime.timezone.utc), null=True),
        ),
        migrations.AlterField(
            model_name='costparameters',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2024, 2, 21, 6, 59, 48, 291015, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='grace',
            name='end_date',
            field=models.DateField(blank=True, default=datetime.datetime(2034, 2, 18, 6, 59, 48, 306640, tzinfo=datetime.timezone.utc), null=True),
        ),
        migrations.AlterField(
            model_name='grace',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2024, 2, 21, 6, 59, 48, 306640, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='onlease',
            name='end_date',
            field=models.DateField(blank=True, default=datetime.datetime(2034, 2, 18, 6, 59, 48, 306640, tzinfo=datetime.timezone.utc), null=True),
        ),
        migrations.AlterField(
            model_name='onlease',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2024, 2, 21, 6, 59, 48, 306640, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='ratecardsurchargevalue',
            name='end_date',
            field=models.DateField(blank=True, default=datetime.datetime(2034, 2, 18, 6, 59, 48, 306640, tzinfo=datetime.timezone.utc), null=True),
        ),
        migrations.AlterField(
            model_name='ratecardsurchargevalue',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2024, 2, 21, 6, 59, 48, 306640, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='thresholddayshift',
            name='end_date',
            field=models.DateField(blank=True, default=datetime.datetime(2034, 2, 18, 6, 59, 48, 306640, tzinfo=datetime.timezone.utc), null=True),
        ),
        migrations.AlterField(
            model_name='thresholddayshift',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2024, 2, 21, 6, 59, 48, 306640, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='thresholdnightshift',
            name='end_date',
            field=models.DateField(blank=True, default=datetime.datetime(2034, 2, 18, 6, 59, 48, 306640, tzinfo=datetime.timezone.utc), null=True),
        ),
        migrations.AlterField(
            model_name='thresholdnightshift',
            name='start_date',
            field=models.DateField(default=datetime.datetime(2024, 2, 21, 6, 59, 48, 306640, tzinfo=datetime.timezone.utc)),
        ),
    ]