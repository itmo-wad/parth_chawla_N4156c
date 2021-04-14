from flask import Flask, render_template, url_for, send_from_directory

app = Flask(__name__)


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route('/misc/<path:path>')
def index(path):
    return app.send_static_file(path)


@app.route('/img/<path:path>')
def index2(path):
    return send_from_directory('static\\img', path)


@app.route('/static/<path:path>')
def index3(path):
    return app.send_static_file(path)


if __name__ == '__main__':
    app.run(debug=True)

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
