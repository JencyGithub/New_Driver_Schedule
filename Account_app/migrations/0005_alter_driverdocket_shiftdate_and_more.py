# Generated by Django 4.2.1 on 2023-12-10 08:07

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account_app', '0004_delete_location_baseplant_baseplanttype_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driverdocket',
            name='shiftDate',
            field=models.DateField(default=datetime.datetime(2023, 12, 10, 8, 7, 53, 412335, tzinfo=datetime.timezone.utc), null=True),
        ),
        migrations.AlterField(
            model_name='holcimdocket',
            name='atPlant',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='holcimdocket',
            name='beginUnload',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='holcimdocket',
            name='endPour',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='holcimdocket',
            name='load',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='holcimdocket',
            name='onJob',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='holcimdocket',
            name='ticketed',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='holcimdocket',
            name='toJob',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='holcimdocket',
            name='toPlant',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='holcimdocket',
            name='wash',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
