import asyncio
from quart import Quart, request, render_template, redirect, url_for
import move_engine
import timer
import hypercorn.asyncio
from hypercorn.config import Config

app = Quart(__name__)

@app.route('/')
async def index():
    return await render_template('index.html')

@app.route('/set_steps', methods=['POST'])
async def set_steps():
    form_data = await request.form
    steps_per_revolution = int(form_data['steps_per_revolution'])
    return redirect(url_for('index'))

@app.route('/calibrate', methods=['POST'])
async def calibrate():
    form_data = await request.form
    calibration_steps = int(form_data['calibration_steps'])
    await move_engine.step(calibration_steps)
    return redirect(url_for('index'))

async def background_timer():
    while True:
        await timer.run()
        await asyncio.sleep(1)

@app.before_serving
async def startup():
    app.add_background_task(background_timer)

if __name__ == '__main__':
    config = Config()
    # Прив'язуємо до конкретного IP-адреси та порту
    config.bind = ["192.168.1.243:5000"]
    asyncio.run(hypercorn.asyncio.serve(app, config))
