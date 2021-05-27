from flask import Flask, render_template, redirect, flash
from secrets import SystemRandom
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.orm import model_form

app = Flask(__name__)
app.secret_key = SystemRandom(SystemRandom, 128)

db = SQLAlchemy(app)

@app.before_first_request
def initDB():
    db.create_all()

class Fish(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)

FishForm = model_form(Fish, db_session = db.session, base_class = FlaskForm)

@app.route('/')
def index():
    title = 'Fishes'
    fishes = Fish.query.all()
    return render_template('index.html', title = title, fishes = fishes)

@app.route('/add', methods = ['GET', 'POST'])

if __name__ == '__main__':
    app.run(debug = True)