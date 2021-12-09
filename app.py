from flask import Flask, render_template, flash, redirect, url_for, request, session
from forms import LoginForm, RegisterForm
from flask_pymongo import PyMongo
from config import Config
import bcrypt
import os

# look inside config.py and add the connection string
app = Flask(__name__)
app.config['MONGO_URI'] = os.environ.get("MONGODB_URI")
app.config.from_object(Config)

mongo = PyMongo(app)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title="Home")


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login handler"""
    if session.get('logged_in'):
        if session['logged_in'] is True:
            return redirect(url_for('index', title="Sign In"))

    form = LoginForm()

    if form.validate_on_submit():
        # get all users
        users = mongo.db.users
        # try and get one with same name as entered
        db_user = users.find_one({'name': request.form['username']})

        if db_user:
            # check password using hashing
            if bcrypt.hashpw(request.form['password'].encode('utf-8'),
                             db_user['password']) == db_user['password']:
                session['username'] = request.form['username']
                session['logged_in'] = True
                # successful redirect to home logged in
                return redirect(url_for('index', title="Sign In", form=form))
            # must have failed set flash message
            flash('Invalid username/password combination')
    return render_template("login.html", title="Sign In", form=form)


@app.route('/logout')
def logout():
    """Clears session and redirects to home"""
    session.clear()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Handles registration functionality"""
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        # get all the users
        users = mongo.db.users
        # see if we already have the entered username
        existing_user = users.find_one({'name': request.form['username']})

        if existing_user is None:
            # hash the entered password
            hash_pass = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())
            # insert the user to DB
            users.insert_one({'name': request.form['username'],
                              'password': hash_pass,
                              'email': request.form['email']})
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        # duplicate username set flash message and reload page
        flash('Sorry, that username is already taken - use another')
        return redirect(url_for('register'))
    return render_template('register.html', title='Register', form=form)


if __name__ == '__main__':
    app.config['TRAP_BAD_REQUEST_ERRORS'] = True
    app.config['DEBUG'] = True
    app.run(host='127.0.0.1', debug=True)
