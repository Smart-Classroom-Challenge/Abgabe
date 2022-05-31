import time
import board
import analogio
import digitalio
import adafruit_dht
import adafruit_scd30
from rgbled import ChainableLED
from ble_interface import BLEConnection

# CO2, Humidity and Temperature
# I2C-1 auf Shield, D23 auf Feather
I2C1 = adafruit_scd30.SCD30(board.I2C())

# Motion
# D4 auf Shield, D9 auf Feather
D4 = digitalio.DigitalInOut(board.D9)
D4.direction = digitalio.Direction.INPUT

# Light
# A0 auf Shield und Feather
A0 = analogio.AnalogIn(board.A0)

# RGB LED
# A2(D16) auf Shield und Feather
A2 = ChainableLED(board.A2, board.A3, 1)

ble_connection = BLEConnection()

while True:
    ble_connection.ble.start_advertising(ble_connection.advertisement)
    turn = True
    while not ble_connection.ble.connected:

        # Indicatior -> BL not connected
        if turn:
            A2.setColorRGB(0, 10, 10)
            turn = False
        else:
            A2.setColorRGB(10, 0, 10)
            turn = True
        time.sleep(1.5)

    while ble_connection.ble.connected:

        # Reading values
        CO2 = int(I2C1.CO2)
        TEMP = int(I2C1.temperature * 100)
        HUMIDITY = int(I2C1.relative_humidity * 100)
        MOTION = bool(D4.value)
        LIGHT = int(A0.value)
        print(CO2, TEMP, HUMIDITY, MOTION, LIGHT)

        dimming_level = 3
        # LED CO2 Stand
        if CO2 < 800:        A2.setColorRGB(  0 //dimming_level, 255//dimming_level,   0//dimming_level) # green
        elif CO2 < 1000:     A2.setColorRGB( 255//dimming_level, 240//dimming_level,   0//dimming_level) # yellow
        elif CO2 < 1400:     A2.setColorRGB( 255//dimming_level, 111//dimming_level,   0//dimming_level) # orange 
        else:                A2.setColorRGB( 255//dimming_level,   0//dimming_level,   0//dimming_level) # red

        # Sending Data
        ble_connection.uart.write("CO2:" + str(CO2) + ":PPM;")
        ble_connection.uart.write("TEM:" + str(TEMP) + ":C;")
        ble_connection.uart.write("HUM:" + str(HUMIDITY) + ":%%rH;")
        ble_connection.uart.write("MOT:" + str(MOTION) + ":BOOL;")
        ble_connection.uart.write("LIG:" + str(LIGHT) + ":NUM;")
        time.sleep(5)
