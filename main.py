import asyncio
from quart import Quart, request, render_template, redirect, url_for
import move_engine  # Повинна містити асинхронну функцію step, що не блокує event loop
import timer        # Повинна містити асинхронну функцію run, яка використовує await asyncio.sleep(), а не time.sleep()
import  os
app = Quart(__name__)
background_task = None

# Визначення шляху до папки для завантаження аудіофайлів
UPLOAD_FOLDER = os.path.join(app.root_path, "music")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # створюємо папку, якщо не існує

@app.route('/')
async def index():
    return await render_template('index.html')

@app.route('/set_steps', methods=['POST'])
async def set_steps():
    form_data = await request.form
    steps_per_revolution = int(form_data['steps_per_revolution'])
    # Можна зберегти це значення за потребою
    return redirect(url_for('index'))

@app.route('/calibrate', methods=['POST'])
async def calibrate():
    form_data = await request.form
    calibration_steps = int(form_data['calibration_steps'])
    await move_engine.step(calibration_steps)  # Асинхронний виклик
    return redirect(url_for('index'))

@app.route('/upload', methods=['POST'])
async def upload_files():
    files = await request.files
    melodiya_file = files.get('melodiya')
    if melodiya_file:
        fixed_filename = "melodiya_audio.mp3"
        file_path = os.path.join(UPLOAD_FOLDER, fixed_filename)
        await asyncio.to_thread(melodiya_file.save, file_path)

    stuk_file = files.get('stuk')
    if stuk_file:
        fixed_filename = "stuk_audio.mp3"
        file_path = os.path.join(UPLOAD_FOLDER, fixed_filename)
        await asyncio.to_thread(stuk_file.save, file_path)


async def background_timer():
    """Фоновий таск, який періодично викликає timer.run().
       Важливо: усі операції повинні бути асинхронними.
    """
    try:
        while True:
            await timer.run()       # Переконайтеся, що у timer.run() замість time.sleep використовується await asyncio.sleep
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
    """Цей метод викликається після завершення роботи сервера для скасування фонового таску."""
    global background_task
    if background_task is not None:
        background_task.cancel()
        try:
            await background_task
        except asyncio.CancelledError:
            print("Background task successfully cancelled.")

if __name__ == '__main__':
    # Запуск застосунку за допомогою ASGI-сервера Hypercorn
    # Наприклад, для запуску:
    # hypercorn main:app --bind 192.168.1.243:5000
    # або запуск через код:
    from hypercorn.config import Config
    import hypercorn.asyncio

    config = Config()
    config.bind = ["192.168.1.243:5000"]
    asyncio.run(hypercorn.asyncio.serve(app, config))
