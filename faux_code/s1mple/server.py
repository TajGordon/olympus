from flask import Flask, render_template, Response
from flask_socketio import SocketIO

app = Flask(__name__)

sio = SocketIO(app)

import cv2
cam = cv2.VideoCapture(0)

# Camera Function
def gen_frames():
    while True:
        success, frame = cam.read()
        if not success:
            break

        # surely theres a better way than jpeg, right?
        # does that even matter...
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield   (b'--frame\r\n'
                 b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/cam')
def camera_feed():
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

import subprocess

@sio.on('run code')
def run_code(code):
    print(f"Executing code: {code}")
    result = subprocess.run(["python", "-c", code], capture_output=True, text=True, timeout=5) 
    sio.emit('code result', {'output': result.stdout})

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    sio.run(app, debug=True, port=5000)
