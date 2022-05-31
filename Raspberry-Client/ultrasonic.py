from grove.grove_ultrasonic_ranger import GroveUltrasonicRanger
import time

sonarleft = GroveUltrasonicRanger(16)
sonarright = GroveUltrasonicRanger(5)

print('Detecting distance...')
while True:
    print('Left: {} cm'.format(sonarleft.get_distance()))
    print('Right: {} cm'.format(sonarright.get_distance()))
    time.sleep(1)
