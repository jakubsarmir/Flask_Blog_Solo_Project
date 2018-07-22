from flask import render_template, url_for, flash, redirect
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog import app, db, bcrypt
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user


data = [

    {
        'post': 'post 1',
        'name': 'jano',
        'date': 'Jul',
        'content': 'abrakadabta'
    },
    {
        'post': 'post 1',
        'name': 'Fero',
        'date': 'januar',
        'content': 'jozo je kral'
    }

]



@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', data=data)


@app.route("/about")
def about():
    return render_template('about.html', title="ABOUT")


@app.route("/register", methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data,password=hashed_pw)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created. You can log in now !', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title="Registration", form=form)


@app.route("/login", methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Unsuccessful log in ! Check your email or password', 'danger')
    return render_template('login.html', title="Login", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
def account():
    return render_template('account.html', title="Account")