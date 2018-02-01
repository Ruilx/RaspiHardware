# -*- coding: utf-8 -*-

import RPi.GPIO as gpio
import time

gpio.setmode(gpio.BCM)
gpio.setup(21, gpio.OUT)
gpio.output(21, gpio.HIGH)
time.sleep(2)
gpio.output(21, gpio.LOW)
gpio.cleanup()
