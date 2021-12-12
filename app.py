from flask import Flask, render_template, url_for
app = Flask(__name__)

app.config['SECRET_KEY'] = '946dafe6e87006141e819258961642b9'

@app.route("/")
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug = True)