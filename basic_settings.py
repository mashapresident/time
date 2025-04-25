from quart import Quart, request, render_template, redirect, url_for, jsonify
from load_config import *
from main import app

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
