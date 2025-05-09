from quart import Quart, request, render_template, redirect, url_for, jsonify
from load_config import *
from main import app, UPLOAD_FOLDER


@app.route('/upload_melody', methods=['POST'])
async def upload_melody():
    files = await request.files
    melody_file = files.get('melody')
    if melody_file:
        fixed_filename = "melody.mp3"
        file_path = os.path.join(UPLOAD_FOLDER, fixed_filename)
        await melody_file.save(file_path)
        return redirect(url_for('index'))
    else:
        return {"error": "No melody sound file provided"}, 400


@app.route('/upload_knock', methods=['POST'])
async def upload_knock():
    files = await request.files
    knock_file = files.get('knock')
    if knock_file:
        fixed_filename = "knock.mp3"
        file_path = os.path.join(UPLOAD_FOLDER, fixed_filename)
        await knock_file.save(file_path)
        return redirect(url_for('index'))
    else:
        return {"error": "No knock sound file provided"}, 400