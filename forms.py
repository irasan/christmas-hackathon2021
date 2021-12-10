from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, RadioField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, Email


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
    child_age = StringField('I am', validators=[DataRequired(),
                                                   Length(min=2, max=10)])
    behaviour = RadioField('This year I have been:',
                            choices=['Naughty', 'Nice',
                                     'A little bit of both'],
                            coerce=str)
    present1 = StringField('What I would like the most this Christmas is...',
                            validators=[DataRequired(), Length(min=2, max=30)])
    present2 = StringField('and', validators=[DataRequired(),
                                                   Length(min=2, max=30)])
    milk = BooleanField('Milk',  false_values=None)
    cookies = BooleanField('Cookies',  false_values=None)
    say_hi = SelectField('P.S. Please say "Hi" to',
                            choices=['Mrs. Clause', 'The Elves',
                                     'Blitzen', 'Comet', 'Cupid',
                                     'Dasher', 'Dancer', 'Donder',
                                     'Prancer', 'Rudolph', 'Vixen'],
                            coerce=str,
                            option_widget=None,
                            validate_choice=True)
    send_letter = SubmitField('Send Letter')