# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import adafruit_ble
from adafruit_ble.services.nordic import UARTService

ble = adafruit_ble.BLERadio()
connection = None

while True:
    print("Scanning for an advertisement...")
    for adv in ble.start_scan(timeout=50, minimum_rssi=-80):
        if adv.complete_name == "CIRCUITPY3137":
            connection = ble.connect(adv)
            print("Connected to:", adv.complete_name)
            break
    ble.stop_scan()

    if connection and connection.connected:
        uart = connection[UARTService]
        while connection.connected:
            message = uart.read()
            if message != None:
                message = message.decode("utf-8").replace("\n", ";")
                if message != "":
                    print(message)
