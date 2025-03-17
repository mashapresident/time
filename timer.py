from datetime import datetime

import move_engine
from move_engine import step
import time
import asyncio


def get_hour():
    return datetime.now().hour


def get_minute():
    return datetime.now().minute


async def run():
    previous_minute = -1  # Початкове значення для перевірки зміни хвилини
    try:
        while True:
            current_minute = get_minute()  # Отримуємо поточну хвилину
            if current_minute != previous_minute:
                #if previous_minute == 60:
                    #звук
                await move_engine.step(70)  # Викликаємо функцію руху двигуна
                previous_minute = current_minute  # Оновлюємо значення хвилини
            time.sleep(50)
    except KeyboardInterrupt:
        print("Програма зупинена користувачем.")
