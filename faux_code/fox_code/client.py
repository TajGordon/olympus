from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)

socketio = SocketIO(app)

@app.route('/test')
def test():
    socketio.emit('test')

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5000)