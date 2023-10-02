from flask import Flask, render_template, Response, jsonify, request
import time
import picar
from picar import back_wheels, front_wheels
import stream

picar.setup()

fw = front_wheels.Front_Wheels(debug=False)
bw = back_wheels.Back_Wheels(debug=False)
bw.ready()
fw.ready()

app = Flask(__name__)

print(stream.start())

SPEED = 60
bw_status = 0

@app.route('/move', methods=['POST']) 
def move():
    data = request.json
    print(data)
    speed = 0
    action = data['move']
    speed = data['speed']
    angle = int(data['turn'])
    if angle < 45:
        angle = 45
    if angle > 135:
        angle = 135
    print(data)
    if action == 'forward':
        bw.speed = speed
        fw.turn(angle)
        bw.forward()
        bw_status = 1
    elif action == 'backward':
        fw.turn(angle)
        bw.speed = speed
        bw.backward()
        bw_status = -1
    elif action == 'stop':
        fw.turn(angle)
        bw.stop()
        bw_status = 0
    return jsonify(isError= False,
                    message= "Success",
                    statusCode= 200,
                    data= data), 200

@app.route('/')
def index():
    host = stream.get_host().decode('utf-8').split(' ')[0]
    """Video streaming home page."""
    return render_template('index.html', host=host)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)