from flask import Flask
from flask import Flask, render_template, flash, redirect
from secrets import SystemRandom


app = Flask(__name__)
app.secret_key = SystemRandom.randbytes(SystemRandom, 128)

@app.route('/')
def index():
    title = 'pw3.1-flask-flash-messages'
    return render_template('index.html', title = title)

@app.route('/hello')
def hello():
    flash('Hello, stranger!')
    return redirect('/')

@app.route('/bye')
def goodbye():
    flash('Bye, stranger!')
    return redirect('/')

if __name__ == '__main__':
    app.run(debug = True)