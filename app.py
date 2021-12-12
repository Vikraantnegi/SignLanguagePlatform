from flask import Flask, render_template, url_for
from forms import RegistrationForm, LoginForm, ContactForm

app = Flask(__name__)

app.config['SECRET_KEY'] = '946dafe6e87006141e819258961642b9'

@app.route("/")
def home():
    form = ContactForm()
    return render_template('home.html', form=form)

@app.route("/register")
def register():
    form = RegistrationForm()
    return render_template('register.html', form=form)

@app.route("/login")
def login():
    form = LoginForm()
    return render_template('login.html', form=form)

if __name__ == '__main__':
    app.run(debug = True)