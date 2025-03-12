import test2
from test2 import *
from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

global steps_per_revolution



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/set_steps', methods=['POST'])
def set_steps():
    steps_per_revolution = int(request.form['steps_per_revolution'])
    test2.step()
    return jsonify({"status": "success"})


@app.route('/calibrate', methods=['POST'])
def calibrate():
    calibration_steps = int(request.form['calibration_steps'])
    test2.step()
    return jsonify({"status": "success"})


def step(direction, steps, delay):
    test2.step()



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
