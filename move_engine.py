#!/usr/bin/env python
"""Basic blinking led example.

The led on A20-OLinuXino-MICRO blinks with a heartbeat-like rate.
"""

import os
import sys
import time
import asyncio
from load_config import  *
import calculator

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


config_data = load_configuration()
steps_per_revolution = config_data.get("steps_per_revolution", 400)
period = config_data.get("period", 5)

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
    steps = min * calculator.get_step_per_minute(steps_per_revolution)
    t = calculator.get_t(calculator.get_step_per_minute(steps_per_revolution), period)
    try:
        if steps > 0:
            wiringpi.digitalWrite(DIR, 1)
            for _ in range(int(steps)):
                wiringpi.digitalWrite(STEP, 1)
                await asyncio.sleep(t)  # асинхронна затримка
                wiringpi.digitalWrite(STEP, 0)
                await asyncio.sleep(t)
        elif steps < 0:
            wiringpi.digitalWrite(DIR, 0)
            for _ in range(int(abs(steps))):
                wiringpi.digitalWrite(STEP, 1)
                await asyncio.sleep(t)
                wiringpi.digitalWrite(STEP, 0)
                await asyncio.sleep(t)
    except asyncio.CancelledError:
        print("Operation cancelled.")
        raise
    except Exception as e:
        print("An error occurred:", e)

