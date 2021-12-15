from flask import Flask, render_template, url_for, flash, redirect, request
from forms import RegistrationForm, LoginForm, ContactForm
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = "946dafe6e87006141e819258961642b9"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.name}', '{self.email}')"


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

if __name__ == '__main__':
    app.run(debug = True)