import subprocess
from flask import Flask, Response
from flask_socketio import SocketIO
import cv2

pi_app = Flask(__name__)
socketio = SocketIO(pi_app, cors_allowed_origins="*")

camera = cv2.VideoCapture(0)

# runs the camera (generates frames)
def gen_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break

        # surely theres a better way than jpeg, right?
        # does that even matter...
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield   (b'--frame\r\n'
                 b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# just the video feed of the camera
@pi_app.route('/pi_video_feed')
def pi_video_feed():
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@socketio.on('connection')
def connection(socket):
    print(socket.id)

# now for code execution
@socketio.on('execute_code')
def execute_code(code):
    # Simple test response (bypass subprocess for testing)
    print(f"Executing code: {code}")
    if code.strip() == "TEST":
        socketio.emit('code_result', {
            'output': "Test successful!", 
            'error': ""
        })
        return

    try:
        result = subprocess.run(['python', '-c', code], 
                                capture_output = True, text=True, timeout=5)
        socketio.emit('code_result',
                      {'output': result.stdout, 'error': result.stderr})
    except Exception as e:
        socketio.emit('code_error', str(e))



if __name__ == '__main__':
    socketio.run(pi_app, debug=True, port=5001)

import atexit

def cleanup():
    camera.release()
    cv2.destroyAllWindows()

atexit.register(cleanup)