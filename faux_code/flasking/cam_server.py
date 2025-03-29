from flask import Flask
import cv2

app = Flask(__name__)

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
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')