from django.contrib.auth.models import User, Group
from .models import Classroom, ConnectionHistory, MeasurementStation, Measurement, EntranceEvent
from rest_framework import viewsets
from rest_framework import permissions
from api.serializers import UserSerializer, GroupSerializer, ClassroomSerializer, MeasurementStationSerializer
from api.serializers import MeasurementsSerializer, ConnectionHistorySerializer, EntranceEventSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class ClassroomViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows classrooms to be viewed or edited.
    """
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer
    permission_classes = [permissions.IsAuthenticated]


class MeasurementStationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows measurement stations to be viewed or edited.
    """
    queryset = MeasurementStation.objects.all()
    serializer_class = MeasurementStationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """GET MeasurementStations for a specific classroom"""
        queryset = MeasurementStation.objects.all()
        fk_classroom = self.request.query_params.get('fk_classroom', None)
        if fk_classroom is not None:
            queryset = queryset.filter(fk_classroom=fk_classroom)
        return queryset


class MeasurementsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows measurements to be viewed or edited.
    """
    queryset = Measurement.objects.all()
    serializer_class = MeasurementsSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """GET Measurements for a specific measurement station"""
        queryset = Measurement.objects.all()
        fk_measurement_station = self.request.query_params.get(
            'fk_measurement_station')
        if fk_measurement_station is not None:
            queryset = queryset.filter(
                fk_measurement_station=fk_measurement_station)
        return queryset


class ConnectionHistoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows connection history to be viewed or edited.
    """
    queryset = ConnectionHistory.objects.all()
    serializer_class = ConnectionHistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        GET ConnectionHistory for a specific measurement station
        If filter_type is set to 'latest', only return latest connection history for given measurement station
        """
        queryset = ConnectionHistory.objects.all()
        fk_measurement_station = self.request.query_params.get(
            'fk_measurement_station')
        filter_type = self.request.query_params.get('filter_type')
        if fk_measurement_station is not None:
            queryset = queryset.filter(
                fk_measurement_station=fk_measurement_station)
        if filter_type is not None and filter_type == 'latest':
            queryset = [queryset.latest('time')]
        return queryset


class EntranceEventViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows entrance events to be viewed or edited.
    """
    queryset = EntranceEvent.objects.all()
    serializer_class = EntranceEventSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """GET EntranceEvents for a specific measurement station"""
        queryset = EntranceEvent.objects.all()
        fk_classroom = self.request.query_params.get('fk_classroom')
        if fk_classroom is not None:
            queryset = queryset.filter(
                fk_measurement_station__fk_classroom=fk_classroom)
        return queryset
