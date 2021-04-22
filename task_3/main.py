from flask import Flask, render_template, url_for, send_from_directory, flash, redirect
from form import RegistrationForm, LoginForm, AfterLogIn
from flask_httpauth import HTTPBasicAuth


app = Flask(__name__)
auth = HTTPBasicAuth()

app.config['SECRET_KEY'] = 'c8dd66edc26b112ab124198bcb575889'


@app.route("/")
@app.route("/home", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'parthchawla65@gmail.com' and form.password.data == 'password':
            return redirect(url_for("cabinet"))
        else:
            flash('Login failed', 'danger')
    return render_template('login.html', title='register', form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'created the account for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Login', form=form)


@app.route("/img")
def index1():
    return app.send_static_file('polo.png')


@app.route('/cabinet/')
def cabinet():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
