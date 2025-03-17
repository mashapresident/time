import asyncio
from quart import Quart, request, render_template, redirect, url_for
import move_engine  # Має async-реалізацію функції step
import timer        # Має async-реалізацію функції run

app = Quart(__name__)
background_task = None  # Глобальна змінна для зберігання таску фонового циклу

@app.route('/')
async def index():
    return await render_template('index.html')

@app.route('/set_steps', methods=['POST'])
async def set_steps():
    form_data = await request.form
    steps_per_revolution = int(form_data['steps_per_revolution'])
    # За потребою: збережіть це значення (наприклад, у глобальній змінній або конфігурації)
    return redirect(url_for('index'))

@app.route('/calibrate', methods=['POST'])
async def calibrate():
    form_data = await request.form
    calibration_steps = int(form_data['calibration_steps'])
    # Викликаємо асинхронну функцію керування двигуном
    await move_engine.step(calibration_steps)
    return redirect(url_for('index'))

async def background_timer():
    """
    Фоновий таск, який працює в одному циклі подій.
    При коректному завершенні (через скасування) ловимо asyncio.CancelledError.
    """
    try:
        while True:
            await timer.run()       # Викликаємо асинхронну функцію таймера
            await asyncio.sleep(1)    # Асинхронне очікування без блокування event loop
    except asyncio.CancelledError:
        print("Background timer cancelled properly.")
        raise

@app.before_serving
async def startup():
    """
    Викликається перед прийомом запитів.
    Запускаємо фоновий таск і зберігаємо посилання на нього для подальшого скасування.
    """
    global background_task
    background_task = asyncio.create_task(background_timer())
    # Альтернативно можна використовувати:
    # app.add_background_task(background_timer)
    # Проте за допомогою asyncio.create_task ми зберігаємо посилання, що дозволяє скасувати задачу.

@app.after_serving
async def shutdown():
    """
    Викликається після завершення роботи сервера.
    Тут скасовуємо фоновий таск, щоб всі асинхронні операції завершились коректно.
    """
    global background_task
    if background_task is not None:
        background_task.cancel()
        try:
            await background_task
        except asyncio.CancelledError:
            print("Background task successfully cancelled.")

if __name__ == '__main__':
    # Запуск застосунку на конкретному IP (наприклад, 192.168.1.243) та порту 5000.
    # Це забезпечує, що сервер слухає лише на вказаній адресі.
    app.run(host='192.168.1.243', port=5000)
