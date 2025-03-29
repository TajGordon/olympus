from flask import Flask, redirect, url_for, request, render_template, Response

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)





































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