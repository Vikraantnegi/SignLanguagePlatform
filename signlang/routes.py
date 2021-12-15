from flask import render_template, url_for, flash, redirect, request
from signlang import app, db, bcrypt
from signlang.forms import RegistrationForm, LoginForm, ContactForm
from signlang.models import User

@app.route("/", methods=['GET','POST'])
def home():
    form = ContactForm(request.form)    
    if form.validate_on_submit():
        flash('Contact Succesfull', 'success')
        return redirect(url_for('home'))     
    return render_template('home.html', form=form)

@app.route("/register", methods=['GET','POST'])
def register():
    form = RegistrationForm(request.form)
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data, email=form.email.data, password=hashed_pwd)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created, Congratulations! Please login to proceed.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route("/login")
def login():
    form = LoginForm()
    return render_template('login.html', form=form)