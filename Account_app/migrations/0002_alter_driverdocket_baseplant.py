# Generated by Django 4.2.2 on 2023-10-12 16:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Account_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='driverdocket',
            name='basePlant',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='Account_app.baseplant'),
        ),
    ]