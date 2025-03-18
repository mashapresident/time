import wiringpi
import asyncio
# Налаштовуємо GPIO-піни
DIR = 6   # GPIO2 - Напрямок
STEP = 11  # GPIO10 - Імпульси
EN = 12    # GPIO2

wiringpi.wiringPiSetup()
wiringpi.pinMode(DIR, 1)
wiringpi.pinMode(STEP, 1)
wiringpi.pinMode(EN, 1)

async def step(steps):
    """
    Асинхронна функція для керування кроками двигуна.
    Блокуючі виклики time.sleep() замінено на await asyncio.sleep().
    """
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


# Приклад використання:
if __name__ == '__main__':
    # Наприклад, потрібно відтворити звук клаку 3 рази після мелодії
    step(100)
