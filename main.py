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
    return jsonify({"status": "success", "steps_per_revolution": steps_per_revolution})


@app.route('/calibrate', methods=['POST'])
def calibrate():
    direction = int(request.form['direction'])
    steps = int(request.form['steps'])
    delay = int(request.form['delay'])
    step(direction, steps, delay)
    return jsonify({"status": "success"})


def step(direction, steps, delay):
    test2.step()



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
