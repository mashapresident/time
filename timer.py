from datetime import datetime
import asyncio
from move_engine import *
import sound

def get_hour():
    return datetime.now().hour

def get_minute():
    return datetime.now().minute

async def run():
    previous_minute = -1
    try:
        while True:
            current_minute = get_minute()
            if current_minute != previous_minute:
                await step(1)
                if previous_minute == 59:
                    previous_minute = current_minute
                    await sound.play(int(get_hour())%12)
            await asyncio.sleep(3)
    except (KeyboardInterrupt, asyncio.CancelledError):
        print("Програма зупинена користувачем.")

# Якщо потрібно запустити код напряму:
if __name__ == '__main__':
    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        print("Програма завершила роботу.")
