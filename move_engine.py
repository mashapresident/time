#!/usr/bin/env python
"""Basic blinking led example.

The led on A20-OLinuXino-MICRO  blinks with rate of 1Hz like "heartbeat".
"""

import os
import sys
import time

if not os.getegid() == 0:
    sys.exit('Script must be run as root')


from time import sleep
from pyA20.gpio import gpio
from pyA20.gpio import port

__author__ = "Stefan Mavrodiev"
__copyright__ = "Copyright 2014, Olimex LTD"
__credits__ = ["Stefan Mavrodiev"]
__license__ = "GPL"
__version__ = "2.0"
__maintainer__ = __author__
__email__ = "support@olimex.com"


def millis():
     return time.time()*1000

#led = port.PA12

DIR = port.PA6  # GPIO2 - Напрямок
STEP = port.PA11  # GPIO10 - Імпульси
EN = port.PA12 # GPIO2

gpio.init()
#gpio.setcfg(led, gpio.OUTPUT)
gpio.setcfg(DIR, gpio.OUTPUT)
gpio.setcfg(STEP, gpio.OUTPUT)
gpio.setcfg(EN, gpio.OUTPUT)

def step(steps):
    if steps > 0:
        gpio.output(DIR, 1)
        try:
           for _ in range(int(steps)):
            gpio.output(STEP, 1)
            time.sleep(0.01)
            gpio.output(STEP, 0)
            time.sleep(0.01)
        except KeyboardInterrupt:
            print ("Goodbye.")

    elif steps < 0:
        gpio.output(DIR, 0)
        steps *= -1
        try:
            for _ in range(int(steps)):
                gpio.output(STEP, 1)
                time.sleep(0.01)
                gpio.output(STEP, 0)
                time.sleep(0.01)

        except KeyboardInterrupt:
            print("Goodbye.")



