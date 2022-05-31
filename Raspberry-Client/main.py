import sys
import pytz
import json
import time
import random
import string
import logging
import threading
import subprocess
import adafruit_ble
import paho.mqtt.publish as publish

from datetime import datetime, timezone
from adafruit_ble.services.nordic import UARTService
from grove.grove_ultrasonic_ranger import GroveUltrasonicRanger

# Variables for Feather
featherconnected = False
feathername = "CIRCUITPY3137"

# Variables for people counter
sonar_left_port = 16
sonar_right_port = 5

# The hostname of the ThingSpeak MQTT broker.
mqtt_host = "mqtt.flespi.io"

# Your MQTT credentials for the device
mqtt_username = "8e0v0tanDPfBzeKkuasrarRQUKwN0WQW0EiPXg2oV6NiaossmIKmXp2HYnlO9ZAZ"
mqtt_password = ""

# Topics
topic_measurement = "fhnw/x/1/measurement"
topic_connectionhistory = "fhnw/x/1/connectionhistory"
topic_peoplecounter = "fhnw/x/1/entranceevent"

# Code
def string_generator(length = 16):
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(length))

def measurement():
    global featherconnected
    mqtt_client_id = string_generator()

    while True:
        try:
            ble = adafruit_ble.BLERadio()
            connection = None

            logging.info("".join(("Measurement: ", "Scanning for Feather...")))
            for adv in ble.start_scan(timeout=50):
                if adv.complete_name == feathername:
                    logging.info("".join(("Measurement: ", "Found:", adv.complete_name, " ... trying to connect")))
                    connection = ble.connect(adv)
                    logging.info("".join(("Measurement: ", "Connected to:", adv.complete_name)))
                    break
            ble.stop_scan()

            if connection and connection.connected:
                featherconnected = True
                uart = connection[UARTService]
                while connection.connected:
                    message = uart.read()
                    if message != None:
                        message = message.decode("utf-8")
                        if message != "":

                            # process valid data
                            data = {
                                "time": str(datetime.now(pytz.timezone("Europe/Zurich"))),
                                "co2": None,
                                "temperature": None,
                                "humidity": None,
                                "motion": None,
                                "light": None
                            }

                            message = message.split(";")
                            for val in message:
                                col = val.split(":")
                                if len(col) == 3:
                                    if col[0] == "CO2":
                                        data["co2"] = col[1]
                                    if col[0] == "TEM":
                                        data["temperature"] = str(int(col[1]) / 100)
                                    if col[0] == "HUM":
                                        data["humidity"] = str(int(col[1]) / 100)
                                    if col[0] == "MOT":
                                        data["motion"] = col[1]
                                    if col[0] == "LIG":
                                        data["light"] = col[1] 

                            # setup data for transmission
                            payload = json.dumps(data)

                            # attempt to publish this data to the topic.
                            try:
                                if not (data["co2"] == None and data ["temperature"] == None and data["humidity"] == None and data["motion"] == None and data["light"] == None):
                                    with open('measurement.txt', 'a') as log:
                                        log.write(payload + "\n")

                                    logging.debug("".join(("Writing Payload = ", payload, " to host: ", mqtt_host, " clientID= ", mqtt_client_id, " User ",
                                        mqtt_username, " PWD ", mqtt_password)))

                                    publish.single(topic_measurement, payload, hostname=mqtt_host, client_id=mqtt_client_id,
                                                auth={'username': mqtt_username, 'password': mqtt_password})
                            except Exception as e:
                                logging.error("".join(("Measurement error: ", str(e))))
                featherconnected = False
        except Exception as e:
            logging.error("".join(("Measurement error: ", str(e))))
            featherconnected = False

def connectionhistory():
    def terminal(cmd):
        stdout, stderr = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
        if stderr != b'':
            raise Exception(stderr.decode('utf-8').replace('\n', ' '))
        return stdout.decode('utf-8').replace('\n', '')

    global featherconnected
    mqtt_client_id = string_generator()
    time.sleep(10)

    while True:
        try:
            data = {
                "time": str(datetime.now(pytz.timezone("Europe/Zurich"))),
                "feather-connected": featherconnected,
                "local-ip": terminal("ip -4 addr show wlan0 | grep -oP '(?<=inet\s)\d+(\.\d+){3}'"),
                "wlan-strength": terminal("iwconfig wlan0 | grep -o 'Signal level=.*'").split('=')[1].split(' ')[0],
                "ping-flespi": terminal("ping -c 1 flespi.io | grep -o 'time=.*'").split('=')[1].split(' ')[0],
                "ping-django": terminal("ping -c 1 django.roulet.dev | grep -o 'time=.*'").split('=')[1].split(' ')[0],
                "ping-grafana": terminal("ping -c 1 grafana.roulet.dev | grep -o 'time=.*'").split('=')[1].split(' ')[0]
            }
            
            # setup data for transmission
            payload = json.dumps(data)
            with open('connectionhistory.txt', 'a') as log:
                log.write(payload + "\n")
            logging.debug("".join(("Writing Payload = ", payload, " to host: ", mqtt_host, " clientID= ", mqtt_client_id, " User ",
                    mqtt_username, " PWD ", mqtt_password)))

            publish.single(topic_connectionhistory, payload, hostname=mqtt_host, client_id=mqtt_client_id,
                            auth={'username': mqtt_username, 'password': mqtt_password})

            time.sleep(60)
        except Exception as e:
            logging.error("".join(("Connection History error: ", str(e))))

def peoplecounter():
    mqtt_client_id = string_generator()

    def current_millis():
        return round(time.time() * 1000)

    def sleep_millis(ms):
        time.sleep(ms/1000)

    def get_distance(sonar, ms_min_wait = 32):
        start = current_millis()
        distance = sonar.get_distance()

        end = current_millis()
        diff = end - start

        if diff < ms_min_wait:
            sleep_millis(ms_min_wait - diff)

        return distance

    def person_infront(sensor):
        if sensor == "right":
            return max(right_arr) > 500 or min(right_arr) < 70
        elif sensor == "left":
            return max(left_arr) > 500 or min(left_arr) < 70
        else:
            raise Exception(f"Unknown sensor: {sensor}")

    def send(payload):
        with open('peoplecounter.txt', 'a') as log_peoplecounter:
            log_peoplecounter.write(payload + "\n")
        logging.debug("".join(("Writing Payload = ", payload, " to host: ", mqtt_host, " clientID= ", mqtt_client_id, " User ",
                    mqtt_username, " PWD ", mqtt_password)))
        publish.single(topic_peoplecounter, payload, hostname=mqtt_host, client_id=mqtt_client_id,
                        auth={'username': mqtt_username, 'password': mqtt_password})

    queue = []

    def on_entrance_event(change):
        queue.append(json.dumps({
            "time": str(datetime.now(pytz.timezone("Europe/Zurich"))),
            "change": change
            }))

    def check_queue():
        while True:
            while len(queue) != 0:
                try:
                    send(queue.pop(0))
                except Exception as e:
                    logging.error("".join(("People counter on entrance event error: ", str(e))))
            sleep_millis(50)

    t = threading.Thread(target=check_queue)
    t.start()

    sonarleft = GroveUltrasonicRanger(sonar_left_port)
    sonarright = GroveUltrasonicRanger(sonar_right_port)

    i = 0
    left_arr  = [0,0,0]
    right_arr = [0,0,0]

    persons = 0
    S = 0
    # S=0: kein Sensor schlägt aus
    # S=1: vor dem linken Sensor ist eine Person, vor dem rechten nicht.
    # S=2: vor dem linken Sensor ist/war eine Person, vor dem rechten Sensor ist eine Person.
    # S=3: vor dem rechten Sensor ist eine Person, vor dem linken nicht.
    # S=4: vor dem rechten Sensor ist/wat eine Person, vor dem linken Sensor ist eine Person.

    while True:
        left_arr[i] = get_distance(sonarleft)
        right_arr[i] = get_distance(sonarright)

        left = person_infront("left")
        right = person_infront("right")

        if S == 0:
            if left: S = 1
            elif right: S = 3
        if S == 1:
            if right: S = 2
            elif left: pass # keep state S = 1
            else: S = 0
        if S == 2 and not right:
            S = 0
            persons += 1
            on_entrance_event(1)
        # same but person comes from the right
        if S == 3:
            if left: S = 4
            elif right: pass # keep state S = 3
            else: S = 0
        if S == 4 and not right:
            S = 0
            persons -= 1
            on_entrance_event(-1)
        #logging.debug("".join(("Personen: ", str(persons))))
        i = (i+1) % 3

def main():
    try:
        logging.basicConfig(filename='main.log', encoding='utf-8', level=logging.INFO)
        logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
        logging.info("--- Program started ---")

        measurement_thread = threading.Thread(target=measurement)
        connectionhistory_thread = threading.Thread(target=connectionhistory)
        peoplecounter_thread = threading.Thread(target=peoplecounter)

        measurement_thread.start()
        logging.info("Measurement Thread started")
        connectionhistory_thread.start()
        logging.info("ConnectionHistory Thread started")
        peoplecounter_thread.start()
        logging.info("People Counter Thread started")

        measurement_thread.join()
        connectionhistory_thread.join()
        peoplecounter_thread.join()

    except KeyboardInterrupt:
        logging.info("--- Program interrupted by KeyboardInterrupt ---")
    finally:
        logging.info("--- Program ended ---")

if __name__ == '__main__':
    main()
