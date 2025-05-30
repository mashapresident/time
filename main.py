import asyncio
import time
from threading import Thread
from werkzeug.utils import secure_filename
from quart import Quart, request, render_template, redirect, url_for, jsonify, session
from load_config import *
from db import engine
from models import *
from timer import run as timer_run
from functools import wraps
from move_engine import *
import move_engine
from task_queue import *

app = Quart(__name__)
app.secret_key = "kpi_clock"



def login_required(f):
    @wraps(f)
    async def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return await f(*args, **kwargs)
    return decorated_function

#ROUTES
@app.route('/')
async def index():
    return redirect(url_for('login'))


@app.route("/login", methods=["GET", "POST"])
async def login():
    if request.method == "POST":
        form = await request.form
        username = form.get("username", "").strip()
        password = form.get("password", "").strip()

        if not username or not password:
            return await render_template("login.html", error="Будь ласка, введіть логін і пароль")

        def check_user(username, password):
            with db.session() as session:
                user = session.query(User).filter(
                    (User.name == username) & (User.password == password)
                ).first()
                return user

        user = await asyncio.to_thread(check_user, username, password)

        if user:
            session["user_id"] = user.id
            return redirect(url_for("main_page"))
        else:
            return await render_template("login.html", error="Невірний логін або пароль")

    return await render_template("login.html")


@app.route('/main_page')
@login_required
async def main_page():
    data = load_configuration()
    steps_per_revolution = data['steps_per_revolution']
    period = data['period']
    
    records = await asyncio.to_thread(get_all_records)  

    return await render_template(
        'main_page.html',
        stp=steps_per_revolution,
        period=period,
        records=records
    )

@app.route('/record', methods=['POST'])
@login_required
async def record():
    return await render_template('add_record.html')


#BASIC SETTINGS
@app.route('/set_steps', methods=['POST'])
async def set_steps():
    form_data = await request.form
    try:
        new_steps = float(form_data['steps_per_revolution'])
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

#MUSIC ACTIONS
@app.route('/save_record', methods=['POST'])
@login_required
async def save_event():
    form = await request.form
    name = form['name']
    repeat = form['repeat']
    time_str = form['time']
    date = ''
    weekday = ''
    priority = 3

    if repeat == 'weekly':
        weekday = form['weekday']
        priority = 2
    elif repeat == 'one-time':
        date = form['date']
        priority = 1

    knock_after = 'knock' in form

    files = await request.files
    audio = files.get('melody')
    if not audio:
        return "Помилка: файл не був завантажений", 400

    filename = secure_filename(audio.filename)
    audio.save(os.path.join(UPLOAD_FOLDER, filename))
    new_event = {
        "date": date,
        "priority": priority,
        "dayOfWeek": weekday,
        "filename": filename,
        "name": name,
        "time": time_str,
        "knockAfter": knock_after
    }
    await asyncio.to_thread(add_record, new_event) 
    return redirect(url_for('main_page'))

@app.route('/delete_record', methods=['POST'])
@login_required
async def delete_record_route():
    form = await request.form
    record_id = form['record_id']
    if record_id:
        await asyncio.to_thread(delete_record, int(record_id))
    return redirect(url_for('main_page'))

@app.route('/upload_regular_records', methods=['POST'])
@login_required
async def upload_regular_melody():
    files = await request.files
    melody_file = files['melody']
    knock_file = files['knock']

    if melody_file:
        melody_file.save(os.path.join(REGULAR_MUSIC_FOLDER, "melody.mp3"))
        print("melody file uploaded")
    else:
        print("no melody file")

    if knock_file:
        knock_file.save(os.path.join(REGULAR_MUSIC_FOLDER, "knock.mp3"))
        print("knock file uploaded")
    else:
        print("no knock file")

    return redirect(url_for('main_page'))


#КАЛІБРУВАННЯ
@app.route('/calibrate_fact', methods=['POST'])
@login_required
async def calibrate_fact():

    try:
        form_data = await request.form
        calibration_time_str = str(form_data['calibration_time'])

        try:
            entered_hour, entered_minute = map(int, calibration_time_str.split(':'))
        except ValueError:
            return jsonify({"error": "Некоректний формат часу. Очікується формат HH:MM."}), 400

        now = time.localtime()
        current_total = now.tm_hour * 60 + now.tm_min
        entered_total = entered_hour * 60 + entered_minute
        difference = current_total - entered_total

        await enqueue_task(fact_calibate, difference)
        return redirect(url_for('main_page'))
    except Exception as e:
        return jsonify({"error": f"Помилка сервера: {e}"}), 500

@app.route('/calibrate', methods=['POST'])
@login_required
async def calibrate():
    form_data = await request.form
    calibration_steps = int(form_data['calibration_steps'])
    try:
        await enqueue_task(move_engine.calibate, calibration_steps)
        print("калібрування на {calibration_steps} кроків")
        return redirect(url_for('main_page'))
    except:
        print("не прокалібрувалось")



@app.before_serving
async def startup():
    init_db(engine)
    asyncio.create_task(process_queue())
    asyncio.create_task(timer_run())

@app.after_serving
async def shutdown():
    print("Shutting down application")



if __name__ == '__main__':
    from hypercorn.config import Config
    import hypercorn.asyncio

    config = Config()
    config.bind = ["10.1.1.250:5000"]
    asyncio.run(hypercorn.asyncio.serve(app, config))