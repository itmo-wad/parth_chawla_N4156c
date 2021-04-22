from flask import Flask, request, send_from_directory, render_template, redirect, make_response
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
auth = HTTPBasicAuth()

users = {
    "user": "123"
}


@auth.verify_password
def verify_password(username, password):
    if username in users:
        return users.get(username) == password
    return False


@app.route('/')
@auth.login_required
def index():
    return app.send_static_file('index.html')


@app.route('/cabinet/')
@auth.login_required
def cabinet():
    return f"Hello user you won a prize"


@app.route('/img')
def img():
    return render_template('image.html')


@app.route('/img/<path:path>')
def index2(path):
    return send_from_directory('static/img', path)  # Send files from current directory


if __name__ == "__main__":
    app.run(host='localhost', port=5000, debug=True)
