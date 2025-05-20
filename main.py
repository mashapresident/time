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