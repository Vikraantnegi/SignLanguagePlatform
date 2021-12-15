from flask import render_template, url_for, flash, redirect, request
from signlang import app
from signlang.forms import RegistrationForm, LoginForm, ContactForm
from signlang.models import User

@app.route("/", methods=['GET','POST'])
def home():
    form = ContactForm(request.form)    
    if form.validate_on_submit():
        flash('Contact Succesfull', 'success')
        return redirect(url_for('home'))     
    return render_template('home.html', form=form)

@app.route("/register")
def register():
    form = RegistrationForm()
    return render_template('register.html', form=form)

@app.route("/login")
def login():
    form = LoginForm()
    return render_template('login.html', form=form)