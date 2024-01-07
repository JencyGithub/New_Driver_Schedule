# Generated by Django 4.2.2 on 2024-01-07 12:09

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('GearBox_app', '0014_alter_clienttruckconnection_startdate_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Account_app', '0038_rctiadjustment_description_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Escalation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('docketNumber', models.CharField(default=None, max_length=10)),
                ('escalationDate', models.DateField(default=None, null=True)),
                ('escalationType', models.CharField(default='', max_length=20)),
                ('remark', models.CharField(default=None, max_length=1024)),
                ('escalationStep', models.PositiveIntegerField(default=1)),
                ('escalationAmount', models.PositiveIntegerField(default=0)),
                ('errorId', models.PositiveIntegerField(default=None)),
                ('clientName', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='GearBox_app.client')),
                ('userId', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='reconciliationreport',
            name='escalationAmount',
        ),
        migrations.RemoveField(
            model_name='reconciliationreport',
            name='escalationStep',
        ),
        migrations.RemoveField(
            model_name='reconciliationreport',
            name='escalationType',
        ),
        migrations.AlterField(
            model_name='driverdocket',
            name='shiftDate',
            field=models.DateField(default=datetime.datetime(2024, 1, 7, 12, 9, 47, 118369, tzinfo=datetime.timezone.utc), null=True),
        ),
        migrations.CreateModel(
            name='EscalationMail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mailTo', models.CharField(default=None, max_length=50)),
                ('mailFrom', models.CharField(default=None, max_length=50)),
                ('mailDescription', models.CharField(default=None, max_length=1024)),
                ('mailType', models.CharField(choices=[('Send', 'Send'), ('Receive', 'Receive')], default='Send', max_length=20)),
                ('mailDate', models.DateField(default=None, null=True)),
                ('mailCount', models.PositiveBigIntegerField(default=1)),
                ('escalationId', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='Account_app.escalation')),
                ('userId', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]