#!/usr/bin/python3

import time
import VL53L0X
import RPi.GPIO as GPIO
from espeak import espeak 

# Create a VL53L0X object
tof = VL53L0X.VL53L0X()

led_blue         = 18
led_green        = 15
led_red          = 14
buzzer = 21

RED   = (True, False, False)
GREEN = (False, True, False)
YELLOW =(False,True,True)
BLUE  = (False, False, True)

tof.start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)# Start ranging
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(led_red,GPIO.OUT)
GPIO.setup(led_green,GPIO.OUT)
GPIO.setup(led_blue,GPIO.OUT)

GPIO.setup(buzzer,GPIO.OUT)

colour = GREEN
phrase = "i need a drink"
wait_time = 0.5         # led change time in seconds 
threshold = 150          # maximum threshold distance in mm
num_of_Beeps = 3
delay_of_beeps = 0.3      # beep delay time in seconds


espeak.synth("Hello, Ready")

def beep( count, delay):
    for x in range (count):
        GPIO.output(buzzer,True)
        time.sleep(.1)
        GPIO.output(buzzer,False)
        time.sleep(delay)

def led_write(_colour = (False,False,False)):
    GPIO.output(led_red,_colour[0])
    GPIO.output(led_green,_colour[1])
    GPIO.output(led_blue,_colour[2])
    
def gesture_routine():
    led_write(colour)
    espeak.synth(phrase)
    beep(num_of_Beeps,delay_of_beeps)
    time.sleep(wait_time)



timing = tof.get_timing()
if (timing < 20000):
    timing = 20000
try:
    while True:
        distance = tof.get_distance()
        if (distance > 0 and distance < threshold):
            gesture_routine()
        else:
            led_write()
        time.sleep(timing/1000000.00)

except KeyboardInterrupt:
    tof.stop_ranging()

