import move_engine
import timer
import asyncio
from quart import Quart, request, render_template, redirect, url_for

app = Quart(__name__)

@app.route('/')
async def index():
    return await render_template('index.html')

@app.route('/set_steps', methods=['POST'])
async def set_steps():
    # Отримуємо дані форми асинхронно
    form_data = await request.form
    steps_per_revolution = int(form_data['steps_per_revolution'])
    return redirect(url_for('index'))

@app.route('/calibrate', methods=['POST'])
async def calibrate():
    # Отримуємо дані форми для калібрування
    form_data = await request.form
    calibration_steps = int(form_data['calibration_steps'])
    # Викликаємо асинхронну функцію для керування двигуном
    await move_engine.step(calibration_steps)
    return redirect(url_for('index'))

async def background_timer():
    while True:
        await timer.run()  # Припускаємо, що timer.run() є асинхронною функцією
        await asyncio.sleep(1)  # Інтервал очікування між викликами

@app.before_serving
async def startup():
    app.add_background_task(background_timer)

if __name__ == '__main__':
    # Запуск застосунку, який слухає усі мережеві інтерфейси (0.0.0.0) на порту 5000.
    # Це означає, що можна підключатися через IP-адресу, наприклад, http://192.168.1.243:5000
    app.run(host='0.0.0.0', port=5000)
