from flask import Flask, Response
from flask_socketio import SocketIO

app = Flask(__name__)

socketio = SocketIO(app, cors_allowed_origins="")

# import cv2
# cap = cv2.VideoCapture(0)
# # The video feed
# def gen_frames():
#     while True:
#         success, frame = cap.read()
#         if not success: break
#         ret, buffer = cv2.imencode('.jpg', frame)
#         frame = buffer.tobytes()
#         yield   (b'--frame\r\n'
#                  b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# @app.route("/video")
# def video_feed():
#     return Response(gen_frames(), mimetype="multipart/x-mixed-replace; boundary=frame")

@socketio.on("test")
def test():
    print("Reached here!")

if __name__ == '__main__':
    socketio.run(app, debug=True, host="0.0.0.0", port=5001)