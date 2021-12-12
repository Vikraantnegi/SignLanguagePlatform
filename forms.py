from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=3, max=30)])
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Your Email', validators=[DataRequired(), Email()])
    password = PasswordField('New Password', validators=[DataRequired()])
    cnfrm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Your Email', validators=[DataRequired(), Email()])
    password = PasswordField('New Password', validators=[DataRequired()])
    remember = BooleanField("Remember Me?")
    submit = SubmitField('Login')

class ContactForm(FlaskForm):
    name = StringField('Name *', validators=[DataRequired(), Length(min=3, max=30)])
    email = StringField('Your Email *', validators=[DataRequired(), Email()])
    phone = StringField('Your Mobile Number *', validators=[DataRequired(), Length(min=10, max=10)])
    extra = StringField('Education / Profession *', validators=[DataRequired(), Length(min=5, max=60)])
    message = TextAreaField('Your Message *', validators=[DataRequired(), Length(min=2, max=200)])
    submit = SubmitField('Let’s Talk')
