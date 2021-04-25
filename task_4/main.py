from flask import Flask, render_template, url_for, send_from_directory, flash, redirect
from form import RegistrationForm, LoginForm, AfterLogIn
from flask_httpauth import HTTPBasicAuth

app = Flask(__name__)
auth = HTTPBasicAuth()

app.config['SECRET_KEY'] = 'c8dd66edc26b112ab124198bcb575889'
app.config['MONGO_DBNAME'] = 'polo'
app.config['MONGO_URI'] = 'mongodb://127.0.0.1:27017/Polo'

mongo = PyMongo(app)


@app.route("/")
@app.route("/home", methods=['GET', 'POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'name': request.form['username']})

    if login_user:
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password'].encode('utf-8')) == login_user['password'].encode('utf-8'):
            session['username'] = request.form['username']
            return redirect(url_for('cabinet'))

    return 'Invalid username/password combination'


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name': request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'name': request.form['username'], 'password': hashpass})
            session['username'] = request.form['username']
            return redirect(url_for('index'))

        return 'That username already exists!'

    return render_template('register.html')


@app.route("/img/")
def index1(path):
    return app.send_static_file(path)


@app.route('/cabinet/')
def cabinet():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
