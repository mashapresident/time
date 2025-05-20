import os
import json

REGULAR_MUSIC_FOLDER = os.path.join(os.getcwd(), "music")
os.makedirs(REGULAR_MUSIC_FOLDER, exist_ok=True)

# конфігурація годинника
CONFIG_FILE = os.path.join(os.getcwd(), "static/config.json")

# куди завантажуємо аудіо
UPLOAD_FOLDER = os.path.join(os.getcwd(), "music/files")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def load_configuration():
    """Завантажує конфігурацію з файлу. Якщо файлу немає — створює його із значенням за замовчуванням."""

    try:
        if not os.path.exists(CONFIG_FILE):
            config = {"steps_per_revolution": 400,
                      "period": 5}
            with open(CONFIG_FILE, "w") as f:
                json.dump(config, f)
            return config
        else:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error loading configuration: {e}")
        return {"steps_per_revolution": 400,
                "period": 5}


def update_config(new_config):
    """Оновлює конфігураційний файл."""
    with open(CONFIG_FILE, "w") as f:
        json.dump(new_config, f)


