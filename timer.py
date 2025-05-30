from datetime import *
import asyncio
import time
from time import sleep
from datetime import date
import move_engine
import player
from models import get_filename
from task_queue import *
def get_hour():
    return datetime.now().hour

def get_minute():
    return datetime.now().minute

def get_day_of_week():
    days_ua = {
        "Monday": "Понеділок",
        "Tuesday": "Вівторок",
        "Wednesday": "Середа",
        "Thursday": "Четвер",
        "Friday": "П'ятниця",
        "Saturday": "Субота",
        "Sunday": "Неділя"
    }
    english_day = datetime.today().strftime('%A')
    return days_ua[english_day]

def get_current_date() -> str:
    return datetime.today().strftime("%d.%m.%Y")

def get_current_time() -> str:
    return datetime.now().strftime("%H:%M")

def run():
    previous_m = -1
    previous_h = -1
    try:
        while True:
            current_m = get_minute()
            current_h = get_hour()

            if current_m != previous_m:
                enqueue_task(move_engine.step, 1)
                print("прохід хвилина")
                date = get_current_date()
                day_of_week = get_day_of_week()
                time = get_current_time()

                filename, knock_after = get_filename(date, day_of_week, time)

                if filename:
                    asyncio.create_task(player.play_melody(filename, knock_after, int(current_h % 12)))
                elif previous_h != current_h and previous_m == 59:
                    asyncio.create_task(player.play_melody("melody.mp3", True, int(current_h % 12)))

            previous_m = current_m
            previous_h = current_h
            time.sleep(0.5)

    except (KeyboardInterrupt, asyncio.CancelledError):
        print("Програму завершено.")