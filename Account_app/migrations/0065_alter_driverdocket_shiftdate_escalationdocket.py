# Generated by Django 4.2.1 on 2024-01-19 04:15

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Account_app', '0064_alter_driverdocket_shiftdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driverdocket',
            name='shiftDate',
            field=models.DateField(default=datetime.datetime(2024, 1, 19, 4, 15, 59, 162828, tzinfo=datetime.timezone.utc), null=True),
        ),
        migrations.CreateModel(
            name='EscalationDocket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('docketNumber', models.CharField(default=None, max_length=10)),
                ('docketDate', models.DateField(default=None, null=True)),
                ('amount', models.IntegerField(default=0)),
                ('remark', models.CharField(default='', max_length=1024)),
                ('escalationId', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='Account_app.escalation')),
            ],
        ),
    ]