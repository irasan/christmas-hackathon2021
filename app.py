from flask import Flask, render_template, flash, redirect, url_for, request, session
from forms import LoginForm, RegisterForm, SmallKidLetterForm, BigKidLetterForm, EditChildForm
from flask_pymongo import PyMongo
from config import Config
import certifi
from bson.objectid import ObjectId
import bcrypt
import os
if os.path.exists("env.py"):
    import env

# look inside config.py and add the connection string
app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config['MONGO_URI'] = os.environ.get("MONGODB_URI")
app.secret_key = os.environ.get("SECRET_KEY")
app.config.from_object(Config)

mongo = PyMongo(app,tlsCAFile=certifi.where())
collection_name = mongo.db.collection_name 

# mongo = PyMongo(app)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title="Home")


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login handler"""
    if session.get('logged_in'):
        if session['logged_in'] is True:
            return redirect(url_for('profile', username=session['username'], title="Sign In"))

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
                return redirect(url_for('index', title="Sign In"))
            # must have failed set flash message
            flash('Invalid username/password combination')
    return render_template("login.html", title="Sign In", form=form)


@app.route("/profile/<username>")
def profile(username):
    if session.get('logged_in'):
        # check if logged in user is the owner of the profile
        if session['logged_in'] is True:
            children = list(mongo.db.children.find({"parent": username}))

            return render_template(
                "profile.html", children=children)
        return redirect(url_for("index"))

    return redirect(url_for("login"))


@app.route("/edit_child/<child_id>", methods=["GET", "POST"])
def edit_child(child_id):
    child = mongo.db.children.find_one({"_id": ObjectId(child_id)})
    form = EditChildForm()
    if "username" in session:
        if request.method == "POST":
            mongo.db.children.find_one_and_update({"_id": ObjectId(child_id)}, 
            { "$set": { "favorite": request.form.get("favorite"), 
                    "nice_thing": request.form.get("nice_thing"),
                    "wanted_behavior": [("do homework", request.form.get("homework")), 
                                    ("be kind", request.form.get("be_kind")),
                                    ("make bed", request.form.get("make_bed")),
                                    ("clean room", request.form.get("clean_room")),
                                    ("go to bed in time", request.form.get("bedtime"))]}})
            return redirect(url_for("profile", username=session["username"]))
        return render_template("edit_child.html", title="Edit Child", child=child, form=form)
    return redirect(url_for("login"))


@app.route("/download_letter")
def download_letter():
    return 


@app.route("/delete_account/<username>")
def delete_account(username):
    if "user" in session:
        mongo.db.users.delete_one({"username": session["username"]})
        mongo.db.children.delete_many({"parent": session["username"]})
        flash("Your Account Was Successfully Deleted")
        return redirect(url_for("index"))

    return redirect(url_for("login"))


@app.route('/get_small_kid_letter', methods=['GET', 'POST'])
def get_small_kid_letter():
    """Render letter template for small kid"""
    form = SmallKidLetterForm(request.form)
    if "username" in session:
        if request.method == "POST":
            child = {
                "name": request.form.get("child_name").lower(),
                "age": request.form.get("child_age"),
                "behaviour": request.form.get("behaviour"),
                "gift1": request.form.get("present1"),
                "gift2": request.form.get("present2"),
                "milk": request.form.get("milk"),
                "cookies": request.form.get("cookies"),
                "say_hi": request.form.get("say_hi"),
                "parent": session['username']
            }
            mongo.db.children.insert_one(child)

            flash("Your Child Was Successfully Added")
            return redirect(url_for("profile", username=session['username']))

        return render_template("letter_small_kid.html", title="Letter To Santa", form=form)
    return render_template("index.html")


@app.route('/get_big_kid_letter', methods=['GET', 'POST'])
def get_big_kid_letter():
    """Render letter template for small kid"""
    form = BigKidLetterForm(request.form)
    if "username" in session:
        if request.method == "POST":
            child = {
                "name": request.form.get("child_name").lower(),
                "age": request.form.get("child_age"),
                "home": request.form.get("home"),
                "homework": request.form.get("homework"),
                "make_bed": request.form.get("make_bed"),
                "brush_teeth": request.form.get("brush_teeth"),
                "clean_room": request.form.get("clean_room"),
                "gift1": request.form.get("present1"),
                "gift2": request.form.get("present2"),
                "gift3": request.form.get("present3"),
                "friend": request.form.get("friend"),
                "say_hi1": request.form.get("say_hi_1"),
                "say_hi2": request.form.get("say_hi_2"),
                "parent": session['username']
            }
            mongo.db.children.insert_one(child)

            flash("Your Child Was Successfully Added")
            return redirect(url_for("profile", username=session['username']))

        return render_template("letter_big_kid.html", title="Letter To Santa", form=form)
    return render_template("index.html")


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
    app.run(host=os.getenv("IP"), 
            port=os.getenv("PORT"), debug=True)
