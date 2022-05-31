from django.apps import AppConfig
from . import mqtt
import sys


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        """
        Called when the django app is ready, starts our MQTT client.
        """
        # See if django is testing
        is_testing = 'test' in sys.argv
        if is_testing:
            return

        # Start the MQTT client
        print('API ready - Initializing MQTT')
        mqtt.client.loop_start()
