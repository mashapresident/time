import asyncio

import load_config
import timer
import time
#import move_engine
from load_config import *
from quart import Quart, request, render_template, redirect, url_for, jsonify
from load_config import *

# Визначення шляху до папки для збереження аудіофайлів "music"
UPLOAD_FOLDER = os.path.join(os.getcwd(), "music")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Шлях до файлу конфігурації
CONFIG_FILE = os.path.join(os.getcwd(), "config.json")
config_data = load_configuration()
steps_per_revolution = config_data.get("steps_per_revolution", 400)

app = Quart(__name__)

@app.route('/calibrate_fact', methods=['POST'])
async def calibrate_fact():
    """Калібрує стрілки годинника на основі часу, введеного користувачем."""
    try:
        form_data = await request.form
        calibration_time_str = str(form_data['calibration_time'])
        try:
            entered_hour, entered_minute = map(int, calibration_time_str.split(':'))
        except ValueError:
            return jsonify({"error": "Некоректний формат часу. Очікується формат HH:MM."}), 400

        now = time.localtime()
        current_hour = now.tm_hour
        current_minute = now.tm_min

        # Перетворення часу в загальну кількість хвилин від початку доби
        entered_total = entered_hour * 60 + entered_minute
        current_total = current_hour * 60 + current_minute

        # Різниця у хвилинах між введеним і поточним часом
        difference = current_total - entered_total

        # Валідація різниці
        if not isinstance(difference, int):
            return jsonify({"error": "Розрахунок часу некоректний."}), 400

        # Виклик функції для калібрування стрілок
     #   await move_engine.fact_calibate(difference)

        return redirect(url_for('index'))
    except Exception as e:
        return jsonify({"error": f"Помилка сервера: {e}"}), 500

@app.route('/upload_melodiya', methods=['POST'])
async def upload_melodiya():
    files = await request.files
    melodiya_file = files.get('melodiya')
    if melodiya_file:
        fixed_filename = "melodiya_audio.mp3"
        file_path = os.path.join(UPLOAD_FOLDER, fixed_filename)
        await melodiya_file.save(file_path)
        return redirect(url_for('index'))
    else:
        return {"error": "No melody sound file provided"}, 400


@app.route('/upload_stuk', methods=['POST'])
async def upload_stuk():
    files = await request.files
    stuk_file = files.get('stuk')
    if stuk_file:
        fixed_filename = "stuk_audio.wav"
        file_path = os.path.join(UPLOAD_FOLDER, fixed_filename)
        await stuk_file.save(file_path)
        return redirect(url_for('index'))
    else:
        return {"error": "No knock sound file provided"}, 400


@app.route('/')
async def index():
    data = load_config.load_configuration()
    steps_per_revolution = data['steps_per_revolution']
    period = data['period']
    return await render_template('index.html', stp=steps_per_revolution, period=period)


@app.route('/set_steps', methods=['POST'])
async def set_steps():
    form_data = await request.form
    try:
        new_steps = int(form_data['steps_per_revolution'])
    except ValueError:
        return "Invalid input", 400

    # Оновлюємо глобальну змінну та конфігураційний файл
    global steps_per_revolution, config_data
    steps_per_revolution = new_steps
    config_data["steps_per_revolution"] = new_steps
    update_config(config_data)

    return redirect(url_for('index'))

@app.route('/set_period', methods=['POST'])
async def set_period():
    form_data = await request.form
    try:
        new_steps = int(form_data['period_per_revolution'])
    except ValueError:
        return "Invalid input", 400

    # Оновлюємо глобальну змінну та конфігураційний файл
    global period, config_data
    period = new_steps
    config_data["period"] = new_steps
    update_config(config_data)

    return redirect(url_for('index'))

@app.route('/calibrate', methods=['POST'])
async def calibrate():
    form_data = await request.form
    calibration_steps = int(form_data['calibration_steps'])
    #await move_engine.calibate(calibration_steps)
    return redirect(url_for('index'))


async def background_timer():
    """Фоновий таск, який періодично викликає timer.run()."""
    try:
        while True:
            await timer.run()
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        print("Background timer cancelled properly.")
        raise


@app.before_serving
async def startup():
    global background_task
    background_task = asyncio.create_task(background_timer())


@app.after_serving
async def shutdown():
    global background_task
    if background_task is not None:
        background_task.cancel()
        try:
            await background_task
        except asyncio.CancelledError:
            print("Background task successfully cancelled.")

@app.route('/add_record', methods=['POST'])
async def add_record():
    form_data = await request.form
    repeat_type = str(form_data[''])
    return redirect(url_for('index'))


if __name__ == '__main__':
    from hypercorn.config import Config
    import hypercorn.asyncio

    config = Config()
    config.bind = ["192.168.1.243:5000"]
    asyncio.run(hypercorn.asyncio.serve(app, config))
