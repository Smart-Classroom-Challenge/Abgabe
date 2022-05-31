# Generated by Django 3.1.14 on 2022-03-16 10:29

from django.db import migrations, models
import django.db.models.deletion
import timescale.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_auto_20220315_1409'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='measurementstation',
            name='ip_address',
        ),
        migrations.CreateModel(
            name='ConnectionHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', timescale.db.models.fields.TimescaleDateTimeField(interval='1 day')),
                ('measurement_time', timescale.db.models.fields.TimescaleDateTimeField(interval='1 millisecond')),
                ('ip_address', models.GenericIPAddressField()),
                ('bluetooth_connected', models.BooleanField(default=False, null=True)),
                ('wlan_signal_strength', models.IntegerField()),
                ('ping_backend', models.IntegerField()),
                ('ping_broker', models.IntegerField()),
                ('fk_measurement_station', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.measurementstation')),
            ],
            options={
                'ordering': ['-measurement_time'],
            },
        ),
    ]