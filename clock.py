import os
import json
import sound
from datetime import datetime
#шлях до папки куди завантажуються файли
UPLOAD_FOLDER = os.path.join(os.getcwd(), "music/files")
#шлях до файлу зі словником
json_file = os.path.join(os.getcwd(), "music/dictionary.json")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def get_melody(date_obj):

    print("f")


def розпарсити_datetime(dt_obj):
    час = dt_obj.time()  # Отримати час
    день_тижня = dt_obj.strftime("%A")  # Отримати назву дня тижня
    дата = dt_obj.date()  # Отримати дату
    рік = dt_obj.year  # Отримати рік

    return час, день_тижня, дата, рік

    # Приклад використання:
now = datetime.now()
час, день_тижня, дата, рік = розпарсити_datetime(now)

print(f"Час: {час}")
print(f"День тижня: {день_тижня}")
print(f"Дата: {дата}")
print(f"Рік: {рік}")
