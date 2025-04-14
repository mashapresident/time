import os
import json
import sound
#шлях до папки куди завантажуються файли
UPLOAD_FOLDER = os.path.join(os.getcwd(), "music/files")
#шлях до файлу зі словником
json_file = os.path.join(os.getcwd(), "music/dictionary.json")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


