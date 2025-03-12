

from flask import Flask, request, render_template, jsonify

app = Flask(__name__)

steps_per_revolution = 200


@app.route('/')
def index():
    return render_template('index.html', steps_per_revolution=steps_per_revolution)


@app.route('/set_steps', methods=['POST'])
def set_steps():
    global steps_per_revolution
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
    # Ваш код для переміщення двигуна
    pass


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
