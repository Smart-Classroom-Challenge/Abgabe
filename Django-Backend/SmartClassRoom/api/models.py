from django.db import models
from timescale.db.models.fields import TimescaleDateTimeField
from timescale.db.models.models import TimescaleModel


class Classroom(models.Model):
    """
    Classroom model
    """
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    room_number = models.CharField(max_length=100)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-name"]


class MeasurementStation(models.Model):
    """
    MeasurementStation model, always connected to a classroom
    """
    fk_classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    active = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-name"]


class Measurement(TimescaleModel):
    """
    Measurement model, always connected to a measurement station
    """
    fk_measurement_station = models.ForeignKey(
        MeasurementStation, on_delete=models.CASCADE)
    insert_time = TimescaleDateTimeField(interval="7 days")
    co2 = models.DecimalField(max_digits=19, decimal_places=10, null=True)
    temperature = models.DecimalField(
        max_digits=19, decimal_places=10, null=True)
    humidity = models.DecimalField(max_digits=19, decimal_places=10, null=True)
    motion = models.BooleanField(default=False, null=True)
    light = models.DecimalField(max_digits=19, decimal_places=10, null=True)

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ["-insert_time"]


class EntranceEvent(TimescaleModel):
    """
    EntranceEvent model, always connected to a measurement station
    """
    fk_measurement_station = models.ForeignKey(
        MeasurementStation, on_delete=models.CASCADE)
    change = models.IntegerField()
    insert_time = TimescaleDateTimeField(interval="7 days")

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ["-insert_time"]


class ConnectionHistory(TimescaleModel):
    """
    ConnectionHistory model, always connected to a measurement station
    """
    fk_measurement_station = models.ForeignKey(
        MeasurementStation, on_delete=models.CASCADE)
    insert_time = TimescaleDateTimeField(interval="7 days")
    ip_address = models.GenericIPAddressField()
    bluetooth_connected = models.BooleanField(default=False, null=True)
    wlan_signal_strength = models.IntegerField()
    ping_backend = models.IntegerField()
    ping_broker = models.IntegerField()
    ping_grafana = models.IntegerField()

    def __str__(self):
        return self.insert_time

    class Meta:
        ordering = ["-insert_time"]
