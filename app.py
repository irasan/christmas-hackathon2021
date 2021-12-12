from flask import Flask, render_template, flash, redirect, url_for, request, session
from forms import LoginForm, RegisterForm, SmallKidLetterForm, BigKidLetterForm, EditChildForm
from flask_pymongo import PyMongo
from config import Config
from fpdf import FPDF
from bson.objectid import ObjectId
from os import listdir
from os.path import isfile, join
import bcrypt
import os
import time

if os.path.exists("env.py"):
    import env

# look inside config.py and add the connection string
app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config['MONGO_URI'] = os.environ.get("MONGODB_URI")
app.secret_key = os.environ.get("SECRET_KEY")
app.config.from_object(Config)

mongo = PyMongo(app)


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title="Home")


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login handler"""
    if "username" in session:
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
    if "username" in session:
        children = list(mongo.db.children.find({"parent": username}))
        return render_template("profile.html", children=children)

    return redirect(url_for("login"))


@app.route("/edit_child/<child_id>", methods=["GET", "POST"])
def edit_child(child_id):
    child = mongo.db.children.find_one({"_id": ObjectId(child_id)})
    form = EditChildForm()
    if "username" in session:
        if request.method == "POST":
            nice_thing = request.form.get("nice_thing")
            favorite = request.form.get("favorite")
            homework = request.form.get("homework")
            be_kind = request.form.get("be_kind")
            make_bed = request.form.get("make_bed")
            clean_room = request.form.get("clean_room")
            bedtime = request.form.get("bedtime")

            mongo.db.children.find_one_and_update({"_id": ObjectId(child_id)}, 
            { "$set": { "favorite": favorite, 
                    "nice_thing": nice_thing,
                    "wanted_behavior": [("do homework, ", homework), 
                                    ("be kind, ", be_kind),
                                    ("make bed, ", make_bed),
                                    ("clean room, ", clean_room),
                                    ("go to bed in time, ", bedtime)]}})
            return redirect(url_for("profile", username=session["username"]))
        return render_template("edit_child.html", title="Edit Child", child=child, form=form)
    return redirect(url_for("login"))


@app.route("/download_response/<child_id>", methods=["GET"])
def download_response(child_id):
    clean_up_pdf_folder(child_id)
    child = mongo.db.children.find_one({"_id": ObjectId(child_id)})
    line_one = f"Dear {child.get('name')}!".title()
    line_two = "Can you believe that Christmas is so close? The North pole is a busy place this time of the year."
    nice_thing = f"I checked my list and I was delighted to see your name on the nice list. I was very impressed how you {child.get('nice_thing')}."
    mylist = []
    for n in child.get('wanted_behavior'):
        if n[1] == 'y':
            mylist.append(n[0])
    wanted_list = ''.join(mylist);
    recommendation = f"Now {wanted_list} and remember the spirit of Christmas all year long!"
    closing = f"Merry Christmas! By the way, {child.get('favorite')} is my favorite too!"
    signature = "Checked twice, \n Santa Claus"

    # save FPDF() class into a variable pdf
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    # Add a page
    pdf.add_page()
    
    pdf.image("static/images/tempred.png", x=0, y=0, w=210, h=297, type='', link='')
    pdf.set_margins(30, 30, 30)
    
    # set style and size of font
    # that you want in the pdf
    pdf.set_font("Arial", size=18)

    # create a cell
    pdf.cell(0, 60, txt=line_one,
             ln=1, align='C')
    # add another cell
    pdf.multi_cell(150, 10, txt=line_two,
             align='L')
    pdf.ln(10)
    pdf.multi_cell(150, 10, txt=nice_thing,
             align='L')
    pdf.multi_cell(150, 10, txt=recommendation,
             align='L')
    pdf.ln(10)
    pdf.multi_cell(150, 10, txt=closing,
             align='L')
    pdf.ln()
    pdf.multi_cell(150, 10, txt=signature,
             align='R')
    # get unique filename
    filename = f"static/pdfs/responseto{child_id}{int(time.time())}.pdf"
    # save the pdf with name .pdf
    pdf.output(filename)
    return redirect(f"../{filename}")


@app.route("/download_letter/<child_id>", methods=["GET"])
def download_letter(child_id):
    clean_up_pdf_folder(child_id)
    child = mongo.db.children.find_one({"_id": ObjectId(child_id)})
    line_three = ""
    behaviour = ""
    behaviour1 = ""
    behaviour2 = ""
    behaviour3 = ""
    behaviour4 = ""
    say_hello = ""
    ps = ""
    line_one = f"Hello, my name is {child.get('name')} and I am {child.get('age')} years old."
    if int(child.get('age')) < 7:
        line_two = "I am really very excited for Christmas this year!"
        if child.get('behaviour', 'Nice') == 'Nice':
            behaviour = "This year I've been good and made lots of good choices."
        elif child.get('behaviour') == 'Naughty':
            behaviour = "This year I know I have made a few bad choices. Even so, "
        else:
            behaviour = "This year I have mostly been good on the whole and"
        gift1 = f"I was hoping you could get me a {child.get('gift1')} and"
        gift2 = f"a {child.get('gift2')}, that would make me so happy!"
        say_hello = f"Please say hi to {child.get('say_hi')} for me."
        last_sentence = ""
        if child.get('milk') == 'y' and child.get('cookies') == 'y':
            last_sentence = "I'm going to leave some milk and cookies for you."
        elif child.get('milk') == 'y':
            last_sentence = "I'm going to leave some milk for when you get here."
        elif child.get('cookies') == 'y':
            last_sentence = "I'm going to leave some cookies for when you get here."
        closing = f"Love, {child.get('name')}"
    else:
        line_two = f"I live in {child.get('home')}, which is quite far from your place in the North Pole"
        line_three = "Christmas is my favourite day of the year, and I am looking forward to your visit in our house."
        behaviour = "You see, I tried my best to be nice this year. The nice things I did are:"
        
        if child.get('brush_teeth') == 'y':
            behaviour1 = "I brushed my teeth everyday"
        if child.get('clean_room') == 'y':
            behaviour2 = "I cleaned my room"
        if child.get('make_bed') == 'y':
            behaviour3 = "I made my bed"
        if child.get('homework') == 'y':
            behaviour4 = "Finished all my homework"
        gift1 = f"This Christmas my wishes are: {child.get('gift1')}, {child.get('gift2')} and {child.get('gift3')}. "
        gift2 = f"I also wish for a {child.get('friend')} for my friend."
        last_sentence = "I love snacking on chocolate pretzels these days, and I'll be leaving a plate of that by the tree."\
            "I hope that will give you energy as you drop off gifts to the other nice kids out there"
        ps = f"P.S. Say 'hi' to {child.get('say_hi1')} and {child.get('say_hi1')} for me!"
        closing = "Merry Christmas, Santa!"
    
    # save FPDF() class into a
    # variable pdf
    pdf = FPDF(orientation='P', unit='mm', format='A4')
    # Add a page
    pdf.add_page()
    if int(child.get('age')) < 7:
        pdf.image("static/images/snowman.jpg", x=0, y=0, w=210, h=297, type='', link='')
    else:
        pdf.image("static/images/balls.jpg", x=0, y=0, w=210, h=297, type='', link='')
    # set style and size of font
    # that you want in the pdf
    pdf.set_font("Arial", size=18)

    # create a cell
    pdf.cell(100, 10, txt="Dear Santa,",
             ln=1, align='L')
    pdf.ln()
    # add another cell
    pdf.cell(200, 10, txt=line_one,
             ln=2, align='L')

    pdf.cell(200, 10, txt=line_two,
             ln=3, align='L')
    if line_three:
        pdf.multi_cell(200, 10, txt=line_three,
             align='L')
    pdf.ln(10)
    pdf.multi_cell(200, 10, txt=behaviour,
             align='L')
    if behaviour1:
        pdf.cell(200, 10, txt=behaviour1,
             ln=6, align='L')
    if behaviour2:
        pdf.cell(200, 10, txt=behaviour2,
             ln=7, align='L')
    if behaviour3:
        pdf.cell(200, 10, txt=behaviour3,
             ln=6, align='R')
    if behaviour4:
        pdf.cell(200, 10, txt=behaviour4,
             ln=7, align='R')       
    pdf.cell(200, 10, txt=gift1,
             ln=8, align='L')
    pdf.cell(200, 10, txt=gift2,
             ln=6, align='L')
    pdf.ln(10)
    if say_hello:
        pdf.cell(200, 10, txt=say_hello,
                ln=9, align='L')
    pdf.multi_cell(200, 10, txt=last_sentence,
             align='L')
    pdf.ln(20)
    pdf.cell(200, 10, txt=closing,
             ln=6, align='C')
    if ps:
        pdf.cell(200, 10, txt=ps,
                 ln=10, align='L')
    # get unique filename
    filename = f"static/pdfs/{child_id}{int(time.time())}.pdf"
    # save the pdf with name .pdf
    pdf.output(filename)
    return redirect(f"../{filename}")


@app.route("/delete_account/<username>")
def delete_account(username):
    if "username" in session:
        mongo.db.users.delete_one({"name": username})
        mongo.db.children.delete_many({"parent": username})
        return redirect(url_for("logout"))

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


@app.route('/countdown')
def countdown():

    return render_template('countdown.html')


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


def clean_up_pdf_folder(child_id):
    """ This function removes any stored pdf for child in order to ensure that their is only
    one per child so the filesystem doesn't get to big"""
    only_pdf_files = [f for f in listdir('static/pdfs/') if isfile(join('static/pdfs/', f))]
    for pdf in only_pdf_files:
        if pdf[:24] == child_id or pdf[10:34] == child_id:
            os.remove(f'static/pdfs/{pdf}')
    return


if __name__ == '__main__':
    app.config['TRAP_BAD_REQUEST_ERRORS'] = True
    app.config['DEBUG'] = True
    app.run(host=os.getenv("IP"), 
            port=os.getenv("PORT"), debug=True)
