#!/usr/bin/env python
"""Basic blinking led example.

The led on A20-OLinuXino-MICRO blinks with a heartbeat-like rate.
"""

import os
import sys
import time
import asyncio


if not os.getegid() == 0:
    sys.exit('Script must be run as root')

import wiringpi

__author__ = "Stefan Mavrodiev"
__copyright__ = "Copyright 2014, Olimex LTD"
__credits__ = ["Stefan Mavrodiev"]
__license__ = "GPL"
__version__ = "2.0"
__maintainer__ = __author__
__email__ = "support@olimex.com"


def millis():
    return time.time() * 1000

# Налаштовуємо GPIO-піни
DIR = 2   # GPIO2 - Напрямок
STEP = 1  # GPIO10 - Імпульси
EN = 0   # GPIO2

wiringpi.wiringPiSetup()
wiringpi.pinMode(DIR, 1)
wiringpi.pinMode(STEP, 1)
wiringpi.pinMode(EN, 1)


async def step(min):
    """
    Асинхронна функція для керування кроками двигуна.
    Блокуючі виклики time.sleep() замінено на await asyncio.sleep().
    """
    steps = int(min * (steps_per_revolution/60))
    try:
        if steps > 0:
            wiringpi.digitalWrite(DIR, 1)
            for _ in range(int(steps)):
                wiringpi.digitalWrite(STEP, 1)
                await asyncio.sleep(0.01)  # асинхронна затримка
                wiringpi.digitalWrite(STEP, 0)
                await asyncio.sleep(0.01)
        elif steps < 0:
            wiringpi.digitalWrite(DIR, 0)
            for _ in range(int(abs(steps))):
                wiringpi.digitalWrite(STEP, 1)
                await asyncio.sleep(0.01)
                wiringpi.digitalWrite(STEP, 0)
                await asyncio.sleep(0.01)
    except asyncio.CancelledError:
        print("Operation cancelled.")
        raise
    except Exception as e:
        print("An error occurred:", e)

