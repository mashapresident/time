import OPi.GPIO as GPIO
import time

GPIO.cleanup()

# Використання фізичної нумерації пінів
GPIO.setmode(GPIO.BOARD)

# Визначаємо піни
DIR = 6  # GPIO2 - Напрямок
STEP = 11  # GPIO10 - Імпульси
EN = 12 # GPIO2

# Налаштування пінів
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)
GPIO.setup(EN, GPIO.OUT)

# Встановлюємо напрямок (1 - вперед, 0 - назад)
GPIO.output(DIR, 1)
GPIO.output(EN, 0)

# Кроковий рух (200 кроків = 1 оберт, якщо 1.8°/крок)
try:
    for _ in range(1600):  # Якщо 1600 імпульсів/оберт
        GPIO.output(STEP, 1)
        time.sleep(0.001)  # Час між імпульсами (чим менше, тим швидше)
        GPIO.output(STEP, 0)
        time.sleep(0.001)

except KeyboardInterrupt:
    print("Зупиняємо двигун...")
    GPIO.cleanup()
