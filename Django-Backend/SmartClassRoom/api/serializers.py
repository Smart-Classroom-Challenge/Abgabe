from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Measurement, Classroom, MeasurementStation, ConnectionHistory, EntranceEvent


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    class Meta:
        model = User
        fields = ['id', 'url', 'username', 'email', 'groups']


class GroupSerializer(serializers.ModelSerializer):
    """Serializer for Group model"""
    class Meta:
        model = Group
        fields = ['id', 'url', 'name']


class ClassroomSerializer(serializers.ModelSerializer):
    """Serializer for Classroom model"""
    class Meta:
        model = Classroom
        fields = ['id', 'url', 'name', 'description',
                  'room_number', 'updated_on']


class MeasurementStationSerializer(serializers.ModelSerializer):
    """Serializer for MeasurementStation model"""
    class Meta:
        model = MeasurementStation
        fields = ['id', 'url', 'fk_classroom', 'name', 'active']


class MeasurementsSerializer(serializers.ModelSerializer):
    """Serializer for Measurement model"""
    class Meta:
        model = Measurement
        fields = [
            'id',
            'url',
            'fk_measurement_station',
            'time',
            'insert_time',
            'co2',
            'temperature',
            'humidity',
            'motion',
            'light']


class ConnectionHistorySerializer(serializers.ModelSerializer):
    """Serializer for ConnectionHistory model"""
    class Meta:
        model = ConnectionHistory
        fields = [
            'id',
            'url',
            'fk_measurement_station',
            'time',
            'insert_time',
            'ip_address',
            'bluetooth_connected',
            'wlan_signal_strength',
            'ping_backend',
            'ping_broker',
            'ping_grafana']


class EntranceEventSerializer(serializers.ModelSerializer):
    """Serializer for EntranceEvent model"""
    class Meta:
        model = EntranceEvent
        fields = ['id', 'url', 'fk_measurement_station',
                  'time', 'insert_time', 'change']
