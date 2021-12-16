import os
import secrets
from keras.optimizers import get
from tensorflow import keras
import tensorflow as tf
from keras.models import load_model
import cv2
import numpy as np
from scipy import stats
import pandas as pd
from flask import render_template, url_for, flash, redirect, request
from signlang import app, db, bcrypt
from signlang.forms import RegistrationForm, LoginForm, ContactForm, UploadForm
from signlang.models import User
from flask_login import login_user, current_user, logout_user, login_required

model = load_model(r'F:\Github\SignLanguagePlatform\signlang\models\SignModel.h5')

words=[
    'book', 'drink', 'computer', 'before', 'chair', 'go', 'clothes',
    'who', 'candy', 'cousin', 'deaf', 'fine', 'help', 'no', 'thin',
    'walk', 'year', 'yes', 'all', 'black', 'cool', 'finish', 'hot',
    'like', 'many', 'mother', 'now', 'orange', 'table', 'thanksgiving',
    'what', 'woman', 'bed', 'blue', 'bowling', 'can', 'dog', 'family',
    'fish', 'graduate', 'hat', 'hearing', 'kiss', 'language', 'later',
    'man', 'shirt', 'study', 'tall', 'white', 'wrong', 'accident',
    'apple', 'bird', 'change', 'color', 'corn', 'cow', 'dance', 'dark',
    'doctor', 'eat', 'enjoy', 'forget', 'give', 'last', 'meet', 'pink',
    'pizza', 'play', 'school', 'secretary', 'short', 'time', 'want',
    'work', 'africa', 'basketball', 'birthday', 'brown', 'but',
    'cheat', 'city', 'cook', 'decide', 'full', 'how', 'jacket',
    'letter', 'medicine', 'need', 'paint', 'paper', 'pull', 'purple',
    'right', 'same', 'son', 'tell', 'thursday', 'visit', 'wait',
    'water', 'wife', 'yellow', 'backpack', 'bar', 'brother', 'cat',
    'check', 'class', 'cry', 'different', 'door', 'green', 'hair',
    'have', 'headache', 'inform', 'knife', 'laugh', 'learn', 'movie',
    'rabbit', 'read', 'red', 'room', 'run', 'show', 'sick', 'snow',
    'take', 'tea', 'teacher', 'week', 'why', 'with', 'write',
    'yesterday', 'again', 'bad', 'ball', 'bathroom', 'blanket', 'buy',
    'call', 'coffee', 'cold', 'college', 'copy', 'cute', 'daughter',
    'example', 'far', 'first', 'friend', 'good', 'happy', 'home',
    'know', 'late', 'leave', 'list', 'lose', 'name', 'old', 'person',
    'police', 'problem', 'remember', 'share', 'soon', 'stay', 'sunday',
    'test', 'tired', 'trade', 'travel', 'window', 'you', 'about',
    'approve', 'arrive', 'balance', 'banana', 'beard', 'because',
    'boy', 'business', 'careful', 'center', 'chat', 'children',
    'christmas', 'clock', 'close', 'convince', 'country', 'crash',
    'day', 'discuss', 'dress', 'drive', 'drop', 'fat', 'feel',
    'football', 'future', 'game', 'girl', 'government', 'hear', 'here',
    'hope', 'house', 'husband', 'interest', 'join', 'light', 'live',
    'make', 'mean', 'more', 'most', 'music', 'new', 'none', 'office',
    'order', 'pants', 'party', 'past', 'pencil', 'plan', 'please',
    'practice', 'president', 'restaurant', 'ride', 'russia', 'salt',
    'sandwich', 'sign', 'since', 'small', 'some', 'south', 'student',
    'teach', 'theory', 'tomato', 'train', 'ugly', 'war', 'where',
    'your', 'always', 'animal', 'argue', 'baby', 'back', 'bake',
    'bath', 'behind', 'bring', 'catch', 'cereal', 'champion', 'cheese',
    'cough', 'crazy', 'delay', 'delicious', 'disappear', 'divorce',
    'draw', 'east', 'easy', 'egg', 'environment', 'father', 'fault',
    'flower', 'friendly', 'glasses', 'halloween', 'hard', 'heart',
    'hour', 'humble', 'hurry', 'improve', 'internet', 'jump', 'kill',
    'law', 'match', 'meat', 'milk', 'money'
]

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

#translate button

def getWord( path ):
    frames=[]
    cap=cv2.VideoCapture(path)
    while(cap.isOpened()):
            ret, frame = cap.read()
            if ret==True:
                try:
                    frame=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    frame = cv2.resize(frame, (96,128), interpolation = cv2.INTER_AREA)
                    frames.append(frame.reshape(128,96,1))
                    
                except:
                    break
            else:
                break
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        
    cap.release()
    cv2.destroyAllWindows()
    frames=np.array(frames)            
    pred=model.predict(frames/255)
    word=stats.mode(np.argmax(pred,axis=1))[0][0]
    word=words[word]
    return word

@app.route("/product", methods=['GET', 'POST'])
@login_required
def product():
    result=""
    videoPath=""
    form = UploadForm()
    if form.validate_on_submit():
        video = form.video.data
        if video:
            if video.filename == '':
                flash('No selected file', 'danger')
                return redirect(request.url)
            else:                
                random_hex = secrets.token_hex(8)
                _, f_ext = os.path.splitext(video.filename)
                video_fn = random_hex + f_ext
                video.save(os.path.join(app.config['UPLOAD_FOLDER'], video_fn))
                videoPath=video_fn
                result = getWord(os.path.join(app.config['UPLOAD_FOLDER'], video_fn))
                flash('Great Success', 'success')
        else:
            flash('No file uploaded', 'danger')
            return redirect(request.url)
    return render_template('product.html', form=form, result=result, video=videoPath)