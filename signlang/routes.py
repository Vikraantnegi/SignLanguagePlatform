import os
from flask import render_template, url_for, flash, redirect, request
from signlang import app, db, bcrypt
from signlang.forms import RegistrationForm, LoginForm, ContactForm, UploadForm
from signlang.models import User
from flask_login import login_user, current_user, logout_user, login_required
from werkzeug.utils import secure_filename

@app.route("/", methods=['GET','POST'])
def home():
    form = ContactForm(request.form)    
    if form.validate_on_submit():
        flash('Contact Succesfull', 'success')
        return redirect(url_for('home'))     
    return render_template('home.html', form=form)

@app.route("/register", methods=['GET','POST'])
def register(): 
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm(request.form)   
    if form.validate_on_submit():
        hashed_pwd = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data, email=form.email.data, password=hashed_pwd)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created, Congratulations! Please login to proceed.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route("/login", methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = db.session.query(User).filter_by(email = form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            nextParam = request.args.get('next')
            if nextParam:
                return redirect(nextParam)
            else:
                return redirect(url_for('home'))
        else:
            flash('Login Unsuccesful. Please check email and password again', 'danger')
    return render_template('login.html', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/product", methods=['POST'])
@login_required
def product():
    form = UploadForm()
    if form.validate_on_submit():
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER']))
        print('Upload_Video: ', + filename)
        flash('Video successfully uploaded and displayed below')
    return render_template('product.html', form=form)