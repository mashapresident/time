import move_engine
from move_engine import *
from flask import Flask, request, render_template, jsonify, redirect, url_for

app = Flask(__name__)

global steps_per_revolution



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/set_steps', methods=['POST'])
def set_steps():
    steps_per_revolution = int(request.form['steps_per_revolution'])
    return redirect(url_for('index'))


@app.route('/calibrate', methods=['POST'])
def calibrate():
    calibration_steps = int(request.form['calibration_steps'])
    move_engine.step(calibration_steps)
    return redirect(url_for('index'))


def step(steps):
    move_engine.step(steps)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
