# Generated by Django 4.0 on 2022-02-26 14:47

from django.db import migrations, models
import django.db.models.deletion
import timescale.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_rename_locaton_messurementstation_location'),
    ]

    operations = [
        migrations.CreateModel(
            name='measurement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', timescale.db.models.fields.TimescaleDateTimeField(interval='1 day')),
                ('measurement_co2', models.DecimalField(decimal_places=10, max_digits=19)),
                ('measurement_temperature', models.DecimalField(decimal_places=10, max_digits=19)),
                ('measurement_humidity', models.DecimalField(decimal_places=10, max_digits=19)),
                ('measurement_time', timescale.db.models.fields.TimescaleDateTimeField(interval='1 sec')),
            ],
            options={
                'ordering': ['-measurement_time'],
            },
        ),
        migrations.CreateModel(
            name='MeasurementStation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=False)),
                ('ip_address', models.GenericIPAddressField()),
                ('station_name', models.CharField(max_length=50)),
            ],
            options={
                'ordering': ['-station_name'],
            },
        ),
        migrations.RemoveField(
            model_name='metric',
            name='Station',
        ),
        migrations.AlterModelOptions(
            name='classroom',
            options={'ordering': ['-name']},
        ),
        migrations.RenameField(
            model_name='classroom',
            old_name='classroom_name',
            new_name='name',
        ),
        migrations.RenameField(
            model_name='classroom',
            old_name='room_number',
            new_name='roomnumber',
        ),
        migrations.AddField(
            model_name='classroom',
            name='updated_on',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.DeleteModel(
            name='MessurementStation',
        ),
        migrations.DeleteModel(
            name='Metric',
        ),
        migrations.AddField(
            model_name='measurementstation',
            name='Classroom',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.classroom'),
        ),
        migrations.AddField(
            model_name='measurement',
            name='Station',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.measurementstation'),
        ),
    ]