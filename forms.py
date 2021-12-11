from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, BooleanField, SubmitField, TextAreaField, RadioField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Length, EqualTo, Email, NumberRange


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),
                                                   Length(min=4, max=20)])
    password = PasswordField('Password',
                             validators=[DataRequired(),
                                         EqualTo('password2', message='Passwords must match')])
    password2 = PasswordField('Repeat Password')
    email = StringField('Email Address', validators=[Length(min=6, max=35)])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Register')


class SmallKidLetterForm(FlaskForm):
    child_name = StringField('My name is', validators=[DataRequired(),
                                                   Length(min=2, max=10)])
    child_age = IntegerField('I am', validators=[NumberRange(min=1, max=6)])
    behaviour = RadioField('This year I have been:',
                            choices=['Naughty', 'Nice',
                                     'A little bit of both'],
                            coerce=str)
    present1 = StringField('What I would like the most this Christmas is a',
                            validators=[DataRequired(), Length(min=2, max=30)])
    present2 = StringField('and a', validators=[DataRequired(),
                                                   Length(min=2, max=30)])
    milk = BooleanField('Milk', false_values=None)
    cookies = BooleanField('Cookies', false_values=None)
    say_hi = SelectField('P.S. Please say "Hi" to',
                            choices=['Mrs. Clause', 'The Elves',
                                     'Blitzen', 'Comet', 'Cupid',
                                     'Dasher', 'Dancer', 'Donder',
                                     'Prancer', 'Rudolph', 'Vixen'],
                            coerce=str,
                            option_widget=None,
                            validate_choice=True)
    submit = SubmitField('Send Letter')


class BigKidLetterForm(FlaskForm):
    child_name = StringField('My name is', validators=[DataRequired(),
                                                   Length(min=2, max=10)])
    child_age = IntegerField('I am', validators=[NumberRange(min=1, max=6)])
    home = StringField('I live in', validators=[DataRequired(),
                                                   Length(min=4, max=16)])
    brush_teeth = BooleanField('Brushed my teeth everyday', false_values=None)
    clean_room = BooleanField('Cleaned my room', false_values=None)
    make_bed = BooleanField('Made my bed', false_values=None)
    homework = BooleanField('Finished all my homework', false_values=None)
    present1 = StringField('This Christmas, my wishes are',
                            validators=[DataRequired(), Length(min=2, max=30)])
    present2 = StringField(',', validators=[DataRequired(), Length(min=2, max=30)])
    present3 = StringField('and', validators=[DataRequired(),
                                                   Length(min=2, max=30)])
    friend = StringField('I also wish for a', validators=[DataRequired(),
                                                   Length(min=2, max=30)])
    say_hi_1 = SelectField('P.S. Say "Hi" to',
                            choices=['Mrs. Clause', 'The Elves'],
                            coerce=str,
                            option_widget=None,
                            validate_choice=True)
    say_hi_2 = SelectField('and',
                            choices=['Blitzen', 'Comet', 'Cupid',
                                     'Dasher', 'Dancer', 'Donder',
                                     'Prancer', 'Rudolph', 'Vixen'],
                            coerce=str,
                            option_widget=None,
                            validate_choice=True)
    submit = SubmitField('Send Letter')


class AddChildForm(FlaskForm):
    child_name = StringField("Child's name", validators=[DataRequired(),
                                                   Length(min=2, max=15)])
    questions = SelectMultipleField('What would you like your child to do more often?',
                            choices=[
                            'Go to bed in time', 'Brush teeth everyday', 'Clean the room',
                            'Make bed', 'Do homework', 'Be kind'])                                               
    # bedtime = BooleanField('Go to bed in time', false_values=None)                                               
    # brush_teeth = BooleanField('Brush teeth everyday', false_values=None)
    # clean_room = BooleanField('Clean the room', false_values=None)
    # make_bed = BooleanField('Make bed', false_values=None)
    # homework = BooleanField('Do homework', false_values=None)
    submit = SubmitField('Add')