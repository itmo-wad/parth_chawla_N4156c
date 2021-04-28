from flask import Flask, render_template, url_for, send_from_directory, flash, redirect, request
from form import RegistrationForm, LoginForm, AfterLogIn, UpdateAccountForm
from flask_httpauth import HTTPBasicAuth
import secrets
from flaskblog.models import User, Post
from flaskblog import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required

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
        if bcrypt.hashpw(request.form['pass'].encode('utf-8'), login_user['password'].encode('utf-8')) == \
                login_user['password'].encode('utf-8'):
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


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/upload/', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/img/")
def index1(path):
    return app.send_static_file(path)


@app.route('/cabinet/', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


if __name__ == '__main__':
    app.run(debug=True)

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
