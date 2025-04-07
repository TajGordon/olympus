from flask import Flask, render_template, Response
from flask_socketio import SocketIO

from picamera2 import Picamera2
import cv2

cam = Picamera2()
config = cam.create_still_configuration()
cam.configure(config)
cam.start()

app = Flask(__name__)
sio = SocketIO(app)

@app.route('/')
def home():
    return "Testing"

def gen_frames():
    while True:
        frame = cam.capture_array()

        frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        # idk what this is


        _, buffer = cv2.imencode('.jpg', frame_bgr)
        
        buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer + b'\r\n')

@app.route('/cam')
def camera_feed():
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    sio.run(app, host="0.0.0.0", port=5000, debug=True)

# Initialize camera with cleanup handler
def cleanup():
    global picam2
    if 'cam' in globals():
        cam.stop()
        cam.close()
import atexit
atexit.register(cleanup)
