import asyncio
import load_config
import timer
import time
from quart import Quart, request, render_template, redirect, url_for, jsonify
from load_config import *
JSON_FILE = 'music/dictionary.json'
# Визначення шляху до папки для збереження аудіофайлів "music"
UPLOAD_FOLDER = os.path.join(os.getcwd(), "music")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
config_data = load_configuration()

app = Quart(__name__)


@app.route('/')
async def index():
    data = load_config.load_configuration()
    steps_per_revolution = data['steps_per_revolution']
    period = data['period']
    return await render_template('index.html', stp=steps_per_revolution, period=period)


@app.route('/add_record')
async def add_record():
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




@app.route('/save_event', methods=['POST'])
async def save_event():
    new_event = request.json
    if not new_event:
        return jsonify({"error": "Invalid data"}), 400

    try:
        with open(JSON_FILE, 'r') as file:
            events = json.load(file)
    except FileNotFoundError:
        events = []

    events.append(new_event)

    with open(JSON_FILE, 'w') as file:
        json.dump(events, file, indent=4)

    return jsonify({"message": "Event saved successfully"}), 200

if __name__ == '__main__':
    from hypercorn.config import Config
    import hypercorn.asyncio

    config = Config()
    config.bind = ["192.168.1.243:5000"]
    asyncio.run(hypercorn.asyncio.serve(app, config))
