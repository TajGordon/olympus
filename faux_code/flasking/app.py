from flask import Flask, redirect, url_for, request, render_template, Response
from flask_socketio import SocketIO, emit
import requests

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    pi_stream = requests.get('http://localhost:5001/pi_video_feed', stream=True)
    return Response(pi_stream.iter_content(chunk_size=1024),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@socketio.on('send code')
def send_code(code):
    print("ho " + code)
    requests.post('http://localhost:5001/execute_code', json={'code': code})

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000)





































# @app.route('/success/<name>')
# def success(name):
#     return 'SUCCESS: %s' % name

# @app.route('/login', methods=['POST', 'GET'])
# def login():
#     if request.method == 'POST':
#         user = request.form['nm']
#         return redirect(url_for('success', name=user))
#     else:
#         user = request.args.get('nm')
#         return redirect(url_for('success', name=user))

# @app.route('/to_login')
# def to_login():
#     return render_template('login.html')

# # stores the camera output
# @app.route('/to_cam')
# def to_cam():
#     # return render_template('cam.html')
#     # Return streaming response (MIME type: multipart/x-mixed-replace)
#     return Response(gen_frames(),
#                    mimetype='multipart/x-mixed-replace; boundary=frame')