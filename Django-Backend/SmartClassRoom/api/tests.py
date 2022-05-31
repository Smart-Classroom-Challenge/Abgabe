from datetime import datetime
from django.test import TestCase
from rest_framework.test import APIClient

from .models import Classroom, MeasurementStation, Measurement, ConnectionHistory, EntranceEvent
from django.contrib.auth.models import User
from rest_framework import status


# No tests for Users and Groups, since we didn't create them.
# (django.contrib.auth.models created them)

class SmartClassroomTestCase(TestCase):
    def setUp(self):
        # create user
        User.objects.create_user(username='admin', password='admin')

        self.client = APIClient()

        response = self.client.post(
            '/api/token/', {'username': 'admin', 'password': 'admin'})
        token = response.data['access']

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)

        Classroom.objects.create(
            name="Classroom 1", description="Description 1", room_number="1")
        Classroom.objects.create(
            name="Classroom 2", description="Description 2", room_number="2")
        Classroom.objects.create(
            name="Classroom 3", description="Description 3", room_number="3")

        classroom_deleted = Classroom.objects.create(
            name="Classroom D", description="Description D", room_number="1")
        self.classroom_deleted_id = classroom_deleted.id
        classroom_deleted.delete()

        MeasurementStation.objects.create(
            fk_classroom=Classroom.objects.get(
                name="Classroom 1"),
            name="Measurement Station 1",
            active=True)
        MeasurementStation.objects.create(
            fk_classroom=Classroom.objects.get(
                name="Classroom 1"),
            name="Measurement Station 2",
            active=True)
        MeasurementStation.objects.create(
            fk_classroom=Classroom.objects.get(
                name="Classroom 2"),
            name="Measurement Station 3",
            active=True)

        measurement_station_1 = MeasurementStation.objects.get(
            name="Measurement Station 1")
        measurement_station_2 = MeasurementStation.objects.get(
            name="Measurement Station 2")

        EntranceEvent.objects.create(
            fk_measurement_station=measurement_station_1,
            time="2020-01-01T00:00:00+01:00",
            insert_time="2020-01-01T00:00:00+01:00",
            change=1)
        EntranceEvent.objects.create(
            fk_measurement_station=measurement_station_1,
            time="2020-01-01T00:01:00+01:00",
            insert_time="2020-01-01T00:01:00+01:00",
            change=-1)
        EntranceEvent.objects.create(
            fk_measurement_station=measurement_station_1,
            time="2020-01-01T00:02:00+01:00",
            insert_time="2020-01-01T00:02:00+01:00",
            change=1)
        EntranceEvent.objects.create(
            fk_measurement_station=measurement_station_2,
            time="2020-01-01T00:00:00+01:00",
            insert_time="2020-01-01T00:00:00+01:00",
            change=-1)

        entrance_event_deleted = EntranceEvent.objects.create(
            fk_measurement_station=measurement_station_1,
            time="2021-01-01T00:02:00+01:00",
            insert_time="2021-01-01T00:02:00+01:00",
            change=1)
        self.entrance_event_deleted_id = entrance_event_deleted.id
        entrance_event_deleted.delete()

        ConnectionHistory.objects.create(
            fk_measurement_station=measurement_station_1,
            time="2020-01-01T00:00:00+01:00",
            insert_time="2020-01-01T00:00:00+01:00",
            ip_address="192.168.1.1",
            bluetooth_connected=True,
            wlan_signal_strength=-65,
            ping_backend=12,
            ping_broker=16,
            ping_grafana=13)
        ConnectionHistory.objects.create(
            fk_measurement_station=measurement_station_1,
            time="2020-01-01T00:01:00+01:00",
            insert_time="2020-01-01T00:01:00+01:00",
            ip_address="192.168.1.1",
            bluetooth_connected=True,
            wlan_signal_strength=-29,
            ping_backend=12,
            ping_broker=15,
            ping_grafana=12)
        ConnectionHistory.objects.create(
            fk_measurement_station=measurement_station_1,
            time="2020-01-01T00:02:00+01:00",
            insert_time="2020-01-01T00:02:00+01:00",
            ip_address="192.168.1.1",
            bluetooth_connected=True,
            wlan_signal_strength=-63,
            ping_backend=12,
            ping_broker=15,
            ping_grafana=12)
        ConnectionHistory.objects.create(
            fk_measurement_station=measurement_station_2,
            time="2020-01-01T00:00:00+01:00",
            insert_time="2020-01-01T00:00:00+01:00",
            ip_address="192.168.1.2",
            bluetooth_connected=False,
            wlan_signal_strength=-84,
            ping_backend=12,
            ping_broker=17,
            ping_grafana=14)

        connection_history_deleted = ConnectionHistory.objects.create(fk_measurement_station=measurement_station_1,
                                                                      time="2021-01-01T00:00:00+01:00",
                                                                      insert_time="2021-01-01T00:00:00+01:00",
                                                                      ip_address="192.168.1.1",
                                                                      bluetooth_connected=True,
                                                                      wlan_signal_strength=-65, ping_backend=12,
                                                                      ping_broker=16, ping_grafana=13)
        self.connection_history_deleted_id = connection_history_deleted.id
        connection_history_deleted.delete()

        Measurement.objects.create(
            fk_measurement_station=measurement_station_1,
            time="2020-01-01T00:00:00+01:00",
            insert_time="2020-01-01T00:00:00+01:00",
            co2=10,
            temperature=20,
            humidity=30,
            motion=True,
            light=True)
        Measurement.objects.create(
            fk_measurement_station=measurement_station_1,
            time="2020-01-01T00:00:00+02:00",
            insert_time="2020-01-01T00:00:00+02:00",
            co2=20,
            temperature=20,
            humidity=30,
            motion=True,
            light=True)
        Measurement.objects.create(
            fk_measurement_station=measurement_station_1,
            time="2020-01-01T00:00:00+03:00",
            insert_time="2020-01-01T00:00:00+03:00",
            co2=30,
            temperature=20,
            humidity=30,
            motion=True,
            light=True)
        Measurement.objects.create(
            fk_measurement_station=measurement_station_2,
            time="2020-01-01T00:00:00+04:00",
            insert_time="2020-01-01T00:00:00+04:00",
            co2=40,
            temperature=20,
            humidity=30,
            motion=True,
            light=True)


class Classroom_Get(SmartClassroomTestCase):
    """
    Tests GET-Endpoint for Classrooms
    """

    def test_get_all_classrooms(self):
        response = self.client.get('/api/Classrooms/', format='json')
        self.assertEqual(len(response.data['results']), 3)
        self.assertEqual(response.data['results'][0]['name'], 'Classroom 3')
        self.assertEqual(response.data['results']
                         [0]['description'], 'Description 3')
        self.assertEqual(response.data['results'][0]['room_number'], '3')

    def test_get_one_classrooms(self):
        classroom_1 = Classroom.objects.get(name='Classroom 1')
        response = self.client.get(
            f'/api/Classrooms/{classroom_1.id}/', format='json')
        self.assertEqual(response.data['name'], 'Classroom 1')
        self.assertEqual(response.data['description'], 'Description 1')
        self.assertEqual(response.data['room_number'], '1')

    def test_get_non_existing_classroom(self):
        response = self.client.get(
            f'/api/Classrooms/{self.classroom_deleted_id}/', format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class Classroom_Post(SmartClassroomTestCase):
    """
    Tests POST-Endpoint for Classrooms
    """

    def test_post_classroom(self):
        self.client.post('/api/Classrooms/',
                         {'name': 'Classroom 4',
                          'description': 'Description 4',
                          'room_number': '4'},
                         format='json')
        classroom_4 = Classroom.objects.get(name='Classroom 4')
        self.assertIsNotNone(classroom_4)
        self.assertEqual(classroom_4.name, 'Classroom 4')
        self.assertEqual(classroom_4.description, 'Description 4')
        self.assertEqual(classroom_4.room_number, '4')

    def test_post_classroom_bad_request_missing(self):
        # missing description, room_number
        response = self.client.post(
            '/api/Classrooms/', {'name': 'Classroom 4'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_classroom_bad_request_format(self):
        # name is not a string, room_number is not a string
        response = self.client.post('/api/Classrooms/',
                                    {'name': 1, 'description': 'Description 4',
                                     'room_number': True},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class Classroom_Delete(SmartClassroomTestCase):
    """
    Tests DELETE-Endpoint for Classrooms
    """

    def test_delete_classroom(self):
        classroom_3 = Classroom.objects.get(name='Classroom 3')
        self.client.delete(f'/api/Classrooms/{classroom_3.id}/', format='json')
        self.assertEqual(Classroom.objects.count(), 2)
        self.assertEqual(Classroom.objects.filter(
            name='Classroom 3').count(), 0)

    def test_delete_classroom_not_found(self):
        # classroom with this id no longer exists
        response = self.client.delete(
            f'/api/Classrooms/{self.classroom_deleted_id}/', format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_classroom_not_found_2(self):
        # id is string instead of int
        response = self.client.delete('/api/Classrooms/asdf/', format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_classroom_not_found_3(self):
        # wrong url format
        response = self.client.delete(
            f'/api/Classrooms/asdf/{self.classroom_deleted_id}/',
            format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class Classroom_Put(SmartClassroomTestCase):
    """
    Tests PUT-Endpoint for Classrooms
    """

    def test_put_classroom(self):
        classroom_1 = Classroom.objects.get(name='Classroom 1')
        self.client.put(
            f'/api/Classrooms/{classroom_1.id}/',
            {
                'name': 'Classroom 1a',
                'description': 'Description 1a',
                'room_number': '1a'},
            format='json')
        classroom_1a = Classroom.objects.get(name='Classroom 1a')
        self.assertIsNotNone(classroom_1a)
        self.assertEqual(classroom_1a.name, 'Classroom 1a')
        self.assertEqual(classroom_1a.description, 'Description 1a')
        self.assertEqual(classroom_1a.room_number, '1a')

    def test_put_classroom_bad_request_missing(self):
        # missing description, room_number
        classroom_1 = Classroom.objects.get(name='Classroom 1')
        response = self.client.put(
            f'/api/Classrooms/{classroom_1.id}/', {'name': 'Classroom 1a'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_classroom_bad_request_format(self):
        # name is as an integer instead of a string, room_number is a boolean
        # instead of a string
        classroom_1 = Classroom.objects.get(name='Classroom 1')
        response = self.client.put(
            f'/api/Classrooms/{classroom_1.id}/',
            {
                'name': 42,
                'description': 'Description 1a',
                'room_number': False},
            format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_classroom_not_found(self):
        # classroom with this id no longer exists
        response = self.client.put(
            f'/api/Classrooms/{self.classroom_deleted_id}/',
            {
                'name': 'Classroom 1a',
                'description': 'Description 1a',
                'room_number': '1a'},
            format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


# CRUD Tests for ConnectionHistory
class ConnectionHistory_Get(SmartClassroomTestCase):
    """
    Tests GET-Endpoint for ConnectionHistory
    """

    def test_get_all_connection_history(self):
        response = self.client.get('/api/ConnectionHistory/', format='json')
        self.assertEqual(len(response.data['results']), 4)
        self.assertEqual(response.data['results']
                         [0]['time'], '2020-01-01T00:02:00+01:00')
        self.assertEqual(response.data['results'][0]
                         ['insert_time'], '2020-01-01T00:02:00+01:00')
        self.assertEqual(response.data['results']
                         [0]['ip_address'], '192.168.1.1')
        self.assertEqual(response.data['results']
                         [0]['bluetooth_connected'], True)
        self.assertEqual(response.data['results']
                         [0]['wlan_signal_strength'], -63)
        self.assertEqual(response.data['results'][0]['ping_backend'], 12)
        self.assertEqual(response.data['results'][0]['ping_broker'], 15)
        self.assertEqual(response.data['results'][0]['ping_grafana'], 12)

    def test_get_filtered_connection_history(self):
        measurement_station_1 = MeasurementStation.objects.get(
            name='Measurement Station 1')
        response = self.client.get(
            f'/api/ConnectionHistory/?fk_measurement_station={measurement_station_1.id}',
            format='json')
        self.assertEqual(len(response.data['results']), 3)
        measurement_station_2 = MeasurementStation.objects.get(
            name='Measurement Station 2')
        response = self.client.get(
            f'/api/ConnectionHistory/?fk_measurement_station={measurement_station_2.id}',
            format='json')
        self.assertEqual(len(response.data['results']), 1)

    def test_get_filtered_latest_connection_history(self):
        measurement_station_1 = MeasurementStation.objects.get(
            name='Measurement Station 1')
        response = self.client.get(
            f'/api/ConnectionHistory/?fk_measurement_station={measurement_station_1.id}&filter_type=latest',
            format='json')
        self.assertEqual(len(response.data['results']), 1)

    def test_get_one_connection_history(self):
        connection_history_1 = ConnectionHistory.objects.get(
            fk_measurement_station=MeasurementStation.objects.get(
                name="Measurement Station 2"))
        response = self.client.get(
            f'/api/ConnectionHistory/{connection_history_1.id}/',
            format='json')
        self.assertEqual(response.data['time'], '2020-01-01T00:00:00+01:00')
        self.assertEqual(
            response.data['insert_time'], '2020-01-01T00:00:00+01:00')
        self.assertEqual(response.data['ip_address'], '192.168.1.2')
        self.assertEqual(response.data['bluetooth_connected'], False)
        self.assertEqual(response.data['wlan_signal_strength'], -84)
        self.assertEqual(response.data['ping_backend'], 12)
        self.assertEqual(response.data['ping_broker'], 17)
        self.assertEqual(response.data['ping_grafana'], 14)

    def test_get_non_existing_connection_history(self):
        response = self.client.get(f'/api/ConnectionHistory/{self.connection_history_deleted_id}/', format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ConnectionHistory_Post(SmartClassroomTestCase):
    """
    Tests POST-Endpoint for ConnectionHistory
    """

    def test_post_connection_history(self):
        measurement_station = MeasurementStation.objects.get(
            name="Measurement Station 3")
        self.client.post('/api/ConnectionHistory/',
                         {'fk_measurement_station': measurement_station.id,
                          'time': '2020-01-01T00:00:00+01:00',
                          'insert_time': '2020-01-01T00:00:00+01:00',
                          'ip_address': '192.168.1.22',
                          'bluetooth_connected': True,
                          'wlan_signal_strength': -63,
                          'ping_backend': 12,
                          'ping_broker': 15,
                          'ping_grafana': 12},
                         format='json')
        connection_history = ConnectionHistory.objects.get(
            fk_measurement_station=measurement_station.id)
        self.assertIsNotNone(connection_history)
        self.assertEqual(connection_history.time, datetime.strptime(
            '2020-01-01T00:00:00+01:00', '%Y-%m-%dT%H:%M:%S%z'))
        self.assertEqual(
            connection_history.insert_time,
            datetime.strptime(
                '2020-01-01T00:00:00+01:00',
                '%Y-%m-%dT%H:%M:%S%z'))
        self.assertEqual(connection_history.ip_address, '192.168.1.22')
        self.assertEqual(connection_history.bluetooth_connected, True)
        self.assertEqual(connection_history.wlan_signal_strength, -63)
        self.assertEqual(connection_history.ping_backend, 12)
        self.assertEqual(connection_history.ping_broker, 15)
        self.assertEqual(connection_history.ping_grafana, 12)

    def test_post_connection_history_bad_request_missing(self):
        measurement_station = MeasurementStation.objects.get(name="Measurement Station 3")
        # missing time, insert_time
        response = self.client.post(
            '/api/ConnectionHistory/', {'fk_measurement_station': measurement_station.id,
                                        'ip_address': '192.168.1.22',
                                        'bluetooth_connected': True,
                                        'wlan_signal_strength': -63,
                                        'ping_backend': 12,
                                        'ping_broker': 15,
                                        'ping_grafana': 12},
            format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_connection_history_bad_request_format(self):
        # fk_measurement_station is not a boolean, wlan_signal_strength is not a string
        response = self.client.post('/api/ConnectionHistory/',
                                    {'fk_measurement_station': True,
                                     'ip_address': 2342,
                                     'bluetooth_connected': True,
                                     'wlan_signal_strength': "hello",
                                     'ping_backend': 12,
                                     'ping_broker': 15,
                                     'ping_grafana': 12},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ConnectionHistory_Delete(SmartClassroomTestCase):
    """
    Tests DELETE-Endpoint for ConnectionHistory
    """

    def test_delete_connection_history(self):
        measurement_station = MeasurementStation.objects.get(
            name="Measurement Station 2")
        connection_history = ConnectionHistory.objects.get(
            fk_measurement_station=measurement_station.id)
        self.client.delete(
            f'/api/ConnectionHistory/{connection_history.id}/', format='json')
        self.assertEqual(ConnectionHistory.objects.count(), 3)
        self.assertEqual(ConnectionHistory.objects.filter(
            fk_measurement_station=measurement_station.id).count(), 0)

    def test_delete_connection_history_not_found(self):
        # connection_history with this id no longer exists
        response = self.client.delete(
            f'/api/ConnectionHistory/{self.connection_history_deleted_id}/', format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_connection_history_not_found_2(self):
        # id is string instead of int
        response = self.client.delete('/api/ConnectionHistory/asdf/', format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_connection_history_not_found_3(self):
        # wrong url format
        response = self.client.delete(
            f'/api/ConnectionHistory/asdf/{self.connection_history_deleted_id}/',
            format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ConnectionHistory_Put(SmartClassroomTestCase):
    """
    Tests PUT-Endpoint for ConnectionHistory
    """

    def test_put_connection_history(self):
        measurement_station_2 = MeasurementStation.objects.get(
            name="Measurement Station 2")
        connection_history_1 = ConnectionHistory.objects.get(
            fk_measurement_station=measurement_station_2.id)
        self.client.put(
            f'/api/ConnectionHistory/{connection_history_1.id}/',
            {
                'fk_measurement_station': measurement_station_2.id,
                'time': '2020-01-01T00:00:00+01:00',
                'insert_time': '2020-01-01T00:00:00+01:00',
                'ip_address': '192.168.1.12',
                'bluetooth_connected': False,
                'wlan_signal_strength': -43,
                'ping_backend': 11,
                'ping_broker': 12,
                'ping_grafana': 11},
            format='json')
        connection_history = ConnectionHistory.objects.get(
            fk_measurement_station=measurement_station_2.id)
        self.assertEqual(connection_history.time, datetime.strptime(
            '2020-01-01T00:00:00+01:00', '%Y-%m-%dT%H:%M:%S%z'))
        self.assertEqual(
            connection_history.insert_time,
            datetime.strptime(
                '2020-01-01T00:00:00+01:00',
                '%Y-%m-%dT%H:%M:%S%z'))
        self.assertEqual(connection_history.ip_address, '192.168.1.12')
        self.assertEqual(connection_history.bluetooth_connected, False)
        self.assertEqual(connection_history.wlan_signal_strength, -43)
        self.assertEqual(connection_history.ping_backend, 11)
        self.assertEqual(connection_history.ping_broker, 12)
        self.assertEqual(connection_history.ping_grafana, 11)

    def test_put_connection_history_bad_request_missing(self):
        # missing time, insert_time
        measurement_station_2 = MeasurementStation.objects.get(name="Measurement Station 2")
        connection_history_1 = ConnectionHistory.objects.get(fk_measurement_station=measurement_station_2.id)
        response = self.client.put(
            f'/api/ConnectionHistory/{connection_history_1.id}/', {'fk_measurement_station': measurement_station_2.id,
                                                                   'ip_address': '192.168.1.12',
                                                                   'bluetooth_connected': False,
                                                                   'wlan_signal_strength': -43, 'ping_backend': 11,
                                                                   'ping_broker': 12, 'ping_grafana': 11},
            format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_connection_history_bad_request_format(self):
        # time is has the wrong time format
        measurement_station_2 = MeasurementStation.objects.get(name="Measurement Station 2")
        connection_history_1 = ConnectionHistory.objects.get(fk_measurement_station=measurement_station_2.id)
        response = self.client.put(
            f'/api/ConnectionHistory/{connection_history_1.id}/',
            {'fk_measurement_station': measurement_station_2.id,
             'time': '01-01-2020T00:00:00+01:00',
             'insert_time': '2020-01-01T00:00:00+01:00',
             'ip_address': '192.168.1.12',
             'bluetooth_connected': False,
             'wlan_signal_strength': -43,
             'ping_backend': 11,
             'ping_broker': 12,
             'ping_grafana': 11},
            format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_connection_history_not_found(self):
        # ConnectionHistory with this id no longer exists
        measurement_station_2 = MeasurementStation.objects.get(name="Measurement Station 2")
        response = self.client.put(
            f'/api/ConnectionHistory/{self.connection_history_deleted_id}/',
            {
                'fk_measurement_station': measurement_station_2.id,
                'time': '2020-01-01T00:00:00+01:00',
                'insert_time': '2020-01-01T00:00:00+01:00',
                'ip_address': '192.168.1.12',
                'bluetooth_connected': False,
                'wlan_signal_strength': -43,
                'ping_backend': 11,
                'ping_broker': 12,
                'ping_grafana': 11},
            format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


# CRUD Tests for MeasurementStation
class MeasurementStation_Get(SmartClassroomTestCase):
    """
    Tests GET-Endpoint for MeasurementStations
    """

    def test_get_measurement_station(self):
        classroom_1 = Classroom.objects.get(name='Classroom 1')
        measurement_station_1 = MeasurementStation.objects.get(
            name='Measurement Station 1')
        response = self.client.get(
            f'/api/MeasurementStations/{measurement_station_1.id}/',
            format='json')
        self.assertEqual(response.data['name'], 'Measurement Station 1')
        self.assertEqual(response.data['active'], True)
        self.assertEqual(response.data['fk_classroom'], classroom_1.id)

    def test_get_nonexisting_measurement_station(self):
        response = self.client.get('/api/MeasurementStations/9999/', format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class MeasurementStation_Post(SmartClassroomTestCase):
    """
    Tests POST-Endpoint for MeasurementStations
    """

    def test_post_measurement_station(self):
        classroom_1 = Classroom.objects.get(name='Classroom 1')
        self.client.post('/api/MeasurementStations/',
                         {'name': 'Measurement Station 4', 'active': True,
                          'fk_classroom': classroom_1.id},
                         format='json')
        measurement_station_4 = MeasurementStation.objects.get(
            name='Measurement Station 4')
        self.assertIsNotNone(measurement_station_4)
        self.assertEqual(measurement_station_4.name, 'Measurement Station 4')
        self.assertEqual(measurement_station_4.active, True)
        self.assertEqual(measurement_station_4.fk_classroom.id, classroom_1.id)

    def test_invalid_station_post(self):
        response = self.client.post('/api/MeasurementStations/',
                                    {'names': 'Measurement Station 4', 'active': True, },
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class MeasurementStation_Delete(SmartClassroomTestCase):
    """
    Tests DELETE-Endpoint for MeasurementStations
    """

    def test_delete_measurement_station(self):
        measurement_station_1 = MeasurementStation.objects.get(
            name='Measurement Station 1')
        self.client.delete(
            f'/api/MeasurementStations/{measurement_station_1.id}/',
            format='json')
        self.assertEqual(MeasurementStation.objects.count(), 2)
        self.assertEqual(MeasurementStation.objects.filter(
            name='Measurement Station 1').count(), 0)

    def test_delete_nonexisting_measurement_station(self):
        response = self.client.delete(
            '/api/MeasurementStations/9999/', format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class MeasurementStation_Put(SmartClassroomTestCase):
    """
    Tests PUT-Endpoint for MeasurementStations
    """

    def test_put_measurement_station(self):
        classroom_2 = Classroom.objects.get(name='Classroom 2')
        measurement_station_1 = MeasurementStation.objects.get(
            name='Measurement Station 1')
        self.client.put(
            f'/api/MeasurementStations/{measurement_station_1.id}/',
            {
                'name': 'Measurement Station 1a',
                'active': False,
                'fk_classroom': classroom_2.id},
            format='json')
        measurement_station_1a = MeasurementStation.objects.get(
            name='Measurement Station 1a')
        self.assertIsNotNone(measurement_station_1a)
        self.assertEqual(measurement_station_1a.name, 'Measurement Station 1a')
        self.assertEqual(measurement_station_1a.active, False)
        self.assertEqual(
            measurement_station_1a.fk_classroom.name, 'Classroom 2')

    def test_put_invalid_measurment_station(self):
        response = self.client.put(
            f'/api/MeasurementStations/99999/',
            {'names': 'test'},
            format='json')
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)


# CRUD Tests for EntranceEvent
class EntranceEvent_Get(SmartClassroomTestCase):
    """
    Tests GET-Endpoint for EntranceEvents
    """

    def test_get_all_entrance_events(self):
        response = self.client.get('/api/EntranceEvents/', format='json')
        measurement_station_1 = MeasurementStation.objects.get(
            name="Measurement Station 1")
        self.assertEqual(response.data['count'], 4)
        self.assertEqual(response.data['results']
                         [0]['time'], '2020-01-01T00:02:00+01:00')
        self.assertEqual(response.data['results'][0]
                         ['insert_time'], '2020-01-01T00:02:00+01:00')
        self.assertEqual(
            response.data['results'][0]['fk_measurement_station'],
            measurement_station_1.id)
        self.assertEqual(response.data['results'][0]['change'], 1)

    def test_get_filtered_entrance_events(self):
        classroom_1 = Classroom.objects.get(name='Classroom 1')
        response = self.client.get(
            f'/api/EntranceEvents/?fk_classroom={classroom_1.id}',
            format='json')
        self.assertEqual(len(response.data['results']), 4)
        classroom_2 = Classroom.objects.get(name='Classroom 2')
        response = self.client.get(
            f'/api/EntranceEvents/?fk_classroom={classroom_2.id}',
            format='json')
        self.assertEqual(len(response.data['results']), 0)

    def test_get_entrance_event_by_id(self):
        measurement_station_1 = MeasurementStation.objects.get(
            name="Measurement Station 2")
        entrance_event = EntranceEvent.objects.get(
            fk_measurement_station=measurement_station_1.id)
        response = self.client.get(
            f'/api/EntranceEvents/{entrance_event.id}/', format='json')
        self.assertEqual(response.data['time'], '2020-01-01T00:00:00+01:00')
        self.assertEqual(
            response.data['insert_time'], '2020-01-01T00:00:00+01:00')
        self.assertEqual(
            response.data['fk_measurement_station'], measurement_station_1.id)
        self.assertEqual(response.data['change'], -1)

    def test_get_nonexistent_entrance_event(self):
        response = self.client.get(
            f'/api/EntranceEvents/{self.entrance_event_deleted_id}/',
            format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class EntranceEvent_Post(SmartClassroomTestCase):
    """
    Tests POST-Endpoint for EntranceEvents
    """

    def test_post_entrance_event(self):
        measurement_station_3 = MeasurementStation.objects.get(
            name="Measurement Station 3")
        self.client.post('/api/EntranceEvents/',
                         {'fk_measurement_station': measurement_station_3.id,
                          'time': '2020-01-01T00:03:00+01:00',
                          'insert_time': '2020-01-01T00:03:00+01:00',
                          'change': 1},
                         format='json')
        self.assertEqual(EntranceEvent.objects.count(), 5)
        self.assertEqual(EntranceEvent.objects.filter(
            fk_measurement_station=measurement_station_3.id).count(), 1)
        entrance_event = EntranceEvent.objects.get(
            fk_measurement_station=measurement_station_3.id)
        self.assertEqual(entrance_event.time, datetime.strptime(
            '2020-01-01T00:03:00+01:00', '%Y-%m-%dT%H:%M:%S%z'))
        self.assertEqual(
            entrance_event.insert_time,
            datetime.strptime(
                '2020-01-01T00:03:00+01:00',
                '%Y-%m-%dT%H:%M:%S%z'))
        self.assertEqual(entrance_event.change, 1)

    def test_post_entrance_event_bad_request_missing(self):
        # missing time
        response = self.client.post('/api/EntranceEvents/',
                                    {'fk_measurement_station': 1,
                                     'insert_time': '2020-01-01T00:03:00+01:00',
                                     'change': 1},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_entrance_event_bad_request_format(self):
        # wrong time format, change needs to be int
        response = self.client.post('/api/EntranceEvents/',
                                    {'fk_measurement_station': 1,
                                     'time': '01-01-2020T00:03:00+01:00',
                                     'insert_time': '2020-01-01T00:03:00+01:00',
                                     'change': "plus eins"},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class EntranceEvent_Delete(SmartClassroomTestCase):
    """
    Tests DELETE-Endpoint for EntranceEvents
    """

    def test_delete_entrance_event(self):
        measurement_station_2 = MeasurementStation.objects.get(
            name="Measurement Station 2")
        entrance_event = EntranceEvent.objects.get(
            fk_measurement_station=measurement_station_2.id)
        self.client.delete(
            f'/api/EntranceEvents/{entrance_event.id}/', format='json')
        self.assertEqual(EntranceEvent.objects.count(), 3)
        self.assertEqual(EntranceEvent.objects.filter(
            fk_measurement_station=measurement_station_2.id).count(), 0)

    def test_delete_entrance_event_not_found(self):
        # entrance_event with this id no longer exists
        response = self.client.delete(
            f'/api/EntranceEvents/{self.entrance_event_deleted_id}/', format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_entrance_event_not_found_2(self):
        # id is string instead of int
        response = self.client.delete(
            f'/api/EntranceEvents/asdf/', format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_entrance_event_not_found_3(self):
        # wrong url format
        response = self.client.delete(
            f'/api/EntranceEvents/asdfd/{self.entrance_event_deleted_id}', format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class EntranceEvent_Put(SmartClassroomTestCase):
    """
    Tests PUT-Endpoint for EntranceEvents
    """

    def test_put_entrance_event(self):
        measurement_station_2 = MeasurementStation.objects.get(
            name="Measurement Station 2")
        entrance_event = EntranceEvent.objects.get(
            fk_measurement_station=measurement_station_2.id)
        self.client.put(
            f'/api/EntranceEvents/{entrance_event.id}/',
            {
                'fk_measurement_station': measurement_station_2.id,
                'time': '2020-01-01T00:01:00+01:00',
                'insert_time': '2020-01-01T00:01:00+01:00',
                'change': 3},
            format='json')
        self.assertEqual(EntranceEvent.objects.count(), 4)
        self.assertEqual(EntranceEvent.objects.filter(
            fk_measurement_station=measurement_station_2.id).count(), 1)
        entrance_event = EntranceEvent.objects.get(
            fk_measurement_station=measurement_station_2.id)
        self.assertEqual(entrance_event.time, datetime.strptime(
            '2020-01-01T00:01:00+01:00', '%Y-%m-%dT%H:%M:%S%z'))
        self.assertEqual(
            entrance_event.insert_time,
            datetime.strptime(
                '2020-01-01T00:01:00+01:00',
                '%Y-%m-%dT%H:%M:%S%z'))
        self.assertEqual(entrance_event.change, 3)

    def test_put_entrance_event_not_found(self):
        # entrance_event with this id no longer exists
        response = self.client.put(
            f'/api/EntranceEvents/{self.entrance_event_deleted_id}/',
            {
                'fk_measurement_station': 1,
                'time': '2020-01-01T00:01:00+01:00',
                'insert_time': '2020-01-01T00:01:00+01:00',
                'change': 3},
            format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_put_entrance_event_bad_request_missing(self):
        # missing time
        measurement_station_2 = MeasurementStation.objects.get(
            name="Measurement Station 2")
        entrance_event = EntranceEvent.objects.get(
            fk_measurement_station=measurement_station_2.id)
        response = self.client.put(
            f'/api/EntranceEvents/{entrance_event.id}/',
            {
                'fk_measurement_station': 1,
                'insert_time': '2020-01-01T00:01:00+01:00',
                'change': 3},
            format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_entrance_event_bad_request_format(self):
        # wrong time format
        measurement_station_2 = MeasurementStation.objects.get(
            name="Measurement Station 2")
        entrance_event = EntranceEvent.objects.get(
            fk_measurement_station=measurement_station_2.id)
        response = self.client.put(
            f'/api/EntranceEvents/{entrance_event.id}/',
            {
                'fk_measurement_station': 1,
                'time': '01-01-2020T00:01:00+01:00',
                'insert_time': '2020-01-01T00:01:00+01:00',
                'change': 3},
            format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class Measurement_Create(SmartClassroomTestCase):
    """
    Tests GET-Endpoint for MeasurementStations
    """

    def test_create_measurement(self):
        measurement_station_1 = MeasurementStation.objects.get(
            name="Measurement Station 1")
        response = self.client.post('/api/Measurements/',
                                    {"fk_measurement_station": measurement_station_1.id,
                                     "time": "2020-02-02T00:00:00+02:00",
                                     "insert_time": "2020-02-02T00:00:00+02:00",
                                     "co2": 10,
                                     "temperature": 20,
                                     "humidity": 30,
                                     "motion": True,
                                     "light": 40000},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        Measurement_1 = Measurement.objects.get(
            time="2020-02-02T00:00:00+02:00")
        self.assertEqual(Measurement_1.time, datetime.strptime(
            '2020-02-02T00:00:00+02:00', '%Y-%m-%dT%H:%M:%S%z'))

    def test_create_invalid_measurment(self):
        response = self.client.post('/api/Measurements/',
                                    {'names': 'test'},
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class Measurement_Read(SmartClassroomTestCase):
    def test_read_measurement(self):
        Measurement_1 = Measurement.objects.get(
            time="2020-01-01T00:00:00+01:00")

        response1 = self.client.get(
            f'/api/Measurements/{Measurement_1.id}/', format='json')

        self.assertEqual(response1.data['time'], '2020-01-01T00:00:00+01:00')

    def test_read_invalid_measurement(self):
        response1 = self.client.get(
            f'/api/Measurements/9999/', format='json')
        self.assertEquals(response1.status_code, status.HTTP_404_NOT_FOUND)


class Measurement_Update(SmartClassroomTestCase):
    def test_put_measurement(self):
        Measurement_1 = Measurement.objects.get(
            time="2020-01-01T00:00:00+01:00")
        MeasurementStation_1 = MeasurementStation.objects.get(
            name="Measurement Station 2")
        response = self.client.put(
            f'/api/Measurements/{Measurement_1.id}/',
            {'id': 1, 'fk_measurement_station': MeasurementStation_1.id,
             'time': '2020-01-01T00:00:00+01:00', 'insert_time': '2020-01-01T00:00:00+01:00', 'co2': 1800,
             'temperature': 21, 'humidity': 33, 'motion': True, 'light': 40000}
            , format='json')
        print(response.status_code, response.status_text, response.reason_phrase)
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['co2'], '1800.0000000000')
        
    def test_put_invalid_measurement(self):
        MeasurementStation_1 = MeasurementStation.objects.get(
            name="Measurement Station 2")
        response = self.client.put(
            f'/api/Measurements/999999/',
            {'id': 99999, 'fk_measurement_station': MeasurementStation_1.id,
             'time': '2020-01-01T00:00:00+01:00', 'insert_time': '2020-01-01T00:00:00+01:00', 'co2': 1800,
             'temperature': 21, 'humidity': 33, 'motion': True, 'light': 40000}
            , format='json')
        print(response.status_code, response.status_text, response.reason_phrase)
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)


class Measurement_Delete(SmartClassroomTestCase):
    def test_delete_measurement(self):
        is_state = Measurement.objects.all().count()
        Measurement_1 = Measurement.objects.get(
            time="2020-01-01T00:00:00+01:00")
        MeasurementStation.objects.get(
            name="Measurement Station 2")
        response = self.client.delete(
            f'/api/Measurements/{Measurement_1.id}/', format='json')
        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(is_state, Measurement.objects.all().count() + 1)

    def test_invalid_delete(self):
        response = self.client.delete(
            f'/api/Measurements/9999/', format='json')
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)
