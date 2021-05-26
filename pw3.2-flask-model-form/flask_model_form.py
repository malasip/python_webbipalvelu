from random import SystemRandom
from flask import Flask, render_template, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from wtforms.ext.sqlalchemy.orm import model_form
from flask_wtf import FlaskForm

app = Flask(__name__)
app.secret_key = SystemRandom.randbytes(SystemRandom, 128)

db = SQLAlchemy(app)

class Animal(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)

@app.before_first_request
def initDB():
    db.create_all()

AnimalForm = model_form(model = Animal, base_class= FlaskForm, db_session = db.session)

@app.route('/')
def index():
    title = 'pw3.2-flask-model-form'
    animals = db.session.query(Animal).all()
    print(animals)
    return render_template('index.html', title = title, animals = animals)

@app.route('/form')
def form():
    title = 'Add new animal'
    form = AnimalForm()
    return render_template('form.html', title = title, form = form)

@app.route('/add', methods = ['POST'])
def add():
    form = AnimalForm()
    animal = Animal()
    form.populate_obj(animal)
    db.session.add(animal)
    db.session.commit()
    flash(f'{animal.name} added to list')
    return redirect('/')

if __name__ == '__main__':
    app.run(debug = True)