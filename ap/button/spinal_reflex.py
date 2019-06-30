#!/usr/bin/env python3

import time
#import RPi.GPIO as GPIO
#import smbus # For I2C

PIN_NUM_SWITCH_IN = 17
PIN_NUM_SWITCH_OUT = 27

#i2c = smbus.SMBus(1)

def switch_callback(gpio_pin):
    print("Switch (GPIO) callback")
    #i2c.write_byte_data()

    
def gpio_initialize():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIN_NUM_SWITCH_IN, GPIO.IN)
    GPIO.setup(PIN_NUM_SWITCH_OUT, GPIO.OUT)
    GPIO.add_event_detect(PIN_NUM_SWITCH_IN,
                          GPIO.RISING,
                          callback=switch_callback,
                          bouncetime=200)
    GPIO.output(PIN_NUM_SWITCH_OUT, GPIO.HIGH)
    
if __name__ == "__main__":
    print('starting spinal reflex...')
    #gpio_initialize()
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        GPIO.cleanup()
