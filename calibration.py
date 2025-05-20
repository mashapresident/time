from quart import Quart, request, render_template, redirect, url_for, jsonify
import time
import move_engine
from main import app
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
