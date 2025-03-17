import move_engine
import timer
from move_engine import *
from timer import run
import asyncio
import asyncio
from quart import Quart, request, render_template, redirect, url_for
import move_engine
import timer

app = Quart(__name__)

@app.route('/')
async def index():
    return await render_template('index.html')

@app.route('/set_steps', methods=['POST'])
async def set_steps():
    form_data = await request.form
    steps_per_revolution = int(form_data['steps_per_revolution'])
    # Можна зберегти значення, яке буде доступне в застосунку
    return redirect(url_for('index'))

@app.route('/calibrate', methods=['POST'])
async def calibrate():
    form_data = await request.form
    calibration_steps = int(form_data['calibration_steps'])
    # Якщо move_engine.step теж є асинхронною функцією:
    await move_engine.step(calibration_steps)
    # Якщо ж функція блокуюча, можна використовувати:
    # await asyncio.to_thread(move_engine.step, calibration_steps)
    return redirect(url_for('index'))

async def background_timer():
    while True:
        await timer.run()  # Припускаємо, що timer.run() є асинхронною функцією
        await asyncio.sleep(1)  # Інтервал очікування між запусками

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(background_timer())
    # Запускаємо застосунок через ASGI-сервер, наприклад, Hypercorn
    import hypercorn.asyncio
    from hypercorn.config import Config
    config = Config()
    config.bind = ["0.0.0.0:5000"]
    loop.run_until_complete(hypercorn.asyncio.serve(app, config))
