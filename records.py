from quart import Quart, request, render_template, redirect, url_for, jsonify
from load_config import *
from main import app, UPLOAD_FOLDER
import json
import os

@app.route('/save_event', methods=['POST'])
async def save_event():
    form = await request.form
    name = form.get('name')
    repeat = form.get('repeat')
    time = form.get('time')
    weekday = form.get('weekday', '')
    date = form.get('date', '')

    new_event = {
        "date": date,
        "dayOfWeek": weekday,
        "filename": "",
        "name": name,
        "time": time
    }



    if not os.path.exists(RECORDS):
        with open(RECORDS, 'w', encoding='utf-8') as f:
            json.dump([], f, ensure_ascii=False, indent=4)

    with open(RECORDS, 'r+', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            data = []
        data.append(new_event)
        f.seek(0)
        json.dump(data, f, ensure_ascii=False, indent=4)
        f.truncate()

    return redirect(url_for('index'))
