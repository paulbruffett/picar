from flask import Flask, render_template, Response, jsonify, request
import cv2
import time
import picar
from picar import back_wheels, front_wheels

picar.setup()

fw = front_wheels.Front_Wheels(debug=False)
bw = back_wheels.Back_Wheels(debug=False)
bw.ready()
fw.ready()

app = Flask(__name__)

camera = cv2.VideoCapture(0)

SPEED = 60
bw_status = 0

def gen_frames():  # generate frame by frame from camera
    while True:
        # Capture frame-by-frame
        success, frame = camera.read()  # read the camera frame
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            time.sleep(0.05)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


@app.route('/video_feed')
def video_feed():
    #Video streaming route. Put this in the src attribute of an img tag
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')

@app.route('/move', methods=['POST']) 
def move():
    data = jsonify(request.json)
    action = data['action']
    speed = data['speed']
    angle = int(data['turn'])
    print(data)
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)