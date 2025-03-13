from datetime import datetime

import move_engine
from move_engine import step
import time


def get_hour():
    return datetime.now().hour


def get_minute():
    return datetime.now().minute


def run():
    previous_minute = -1  # Початкове значення для перевірки зміни хвилини

    try:
        while True:
            current_minute = get_minute()  # Отримуємо поточну хвилину

            if current_minute != previous_minute:
                move_engine.step(70)  # Викликаємо функцію руху двигуна
                previous_minute = current_minute  # Оновлюємо значення хвилини

            time.sleep(1)  # Перевірка кожну секунду
    except KeyboardInterrupt:
        print("Програма зупинена користувачем.")
