import asyncio
from crypt import methods
from werkzeug.utils import secure_filename
from quart import Quart, request, render_template, redirect, url_for, jsonify
from load_config import *
from record_model import *
from timer import run
app = Quart(__name__)

@app.route('/')
async def index():
    data = load_configuration()
    steps_per_revolution = data['steps_per_revolution']
    period = data['period']
    records = await get_all_records()
    return await render_template('index.html', stp=steps_per_revolution, period=period, records=records)

@app.route('/record', methods=['POST'])
async def record():
    return await render_template('add_record.html')


async def background_timer():
    """Фоновий таск, який періодично викликає timer.run()."""
    try:
        while True:
            await timer.run()
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        print("Background timer cancelled properly.")
        raise

@app.route('/save_record', methods=['POST'])
async def save_event():
    if request.method == 'POST':
        print(await request.form)
        form = await request.form
        name = form['name']
        repeat = form['repeat']
        time = form['time']
        date = ''
        weekday = ''
        priority = 3
        if  repeat == 'weekly':
            weekday = form['weekday']
            priority = 2
        elif repeat == 'one-time':
            date = form['date']
            priority = 1
        if 'knock' in form:
            knock_after = 1
        else:
            knock_after = 0
        files = await request.files
        if 'melody' not in files:
            return "Помилка: файл не був завантажений", 400
        audio =  files['melody']
        filename = secure_filename(audio.filename)
        await audio.save(os.path.join(UPLOAD_FOLDER, filename))
        new_event = {
            "date": date,
            "priority": priority,
            "dayOfWeek": weekday,
            "filename": filename,
            "name": name,
            "time": time,
            "knockAfter": knock_after
        }
        await add_record(new_event)
    return redirect(url_for('index'))

@app.route('/delete_record', methods=['POST'])
async def delete_record():
    print(await request.form)
    form = await request.form
    record_id = form['record_id']
    if record_id:
        await delete(int(record_id))
    return redirect(url_for('index'))

@app.route('/upload_regular_records', methods=['POST'])
async def upload_regular_melody():
    if request.method == 'POST':
        print(await request.files)
        files = await request.files
        melody_file = files['melody']
        knock_file = files['knock']
        if melody_file:
            fixed_filename = "melody.mp3"
            file_path = os.path.join(REGULAR_MUSIC_FOLDER, fixed_filename)
            await melody_file.save(file_path)
            print("melody file")
        else:
            print("no melody file")
        if knock_file:
            fixed_filename = secure_filename("knock.mp3")
            file_path = os.path.join(REGULAR_MUSIC_FOLDER, fixed_filename)
            await knock_file.save(file_path)
            print("knock file")
        else:
            print("no knock file")
    return redirect(url_for('index'))

@app.before_serving
async def startup():
    await init_db()
    asyncio.create_task(run())

@app.after_serving
async def shutdown():
    global background_task
    if background_task is not None:
        background_task.cancel()
        try:
            await background_task
        except asyncio.CancelledError:
            print("Background task successfully cancelled.")
import time
import move_engine
from move_engine import *

#калібрування за поточним часом
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
        await move_engine.fact_calibate(difference)

        return redirect(url_for('index'))
    except Exception as e:
        return jsonify({"error": f"Помилка сервера: {e}"}), 500


@app.route('/calibrate', methods=['POST'])
async def calibrate():
    form_data = await request.form
    calibration_steps = int(form_data['calibration_steps'])
    await move_engine.calibate(calibration_steps)
    return redirect(url_for('index'))


if __name__ == '__main__':
    from hypercorn.config import Config
    import hypercorn.asyncio

    config = Config()
    config.bind = ["10.1.1.250:5000"]
    asyncio.run(hypercorn.asyncio.serve(app, config))