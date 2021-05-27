from flask import Flask, render_template, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.orm import model_form
from secrets import SystemRandom

app = Flask(__name__)
app.secret_key = SystemRandom.randbytes(SystemRandom, 128)

db = SQLAlchemy(app)

class Album(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    artist = db.Column(db.String, nullable = False)
    released = db.Column(db.Integer, nullable = False)

AlbumForm = model_form(Album, base_class = FlaskForm, db_session = db.session)

@app.before_first_request
def initDB():
    db.create_all()

@app.route('/')
def index():
    title = 'CD database'
    albums = Album.query.all()
    return render_template('index.html', title = title, albums = albums)

@app.route('/add', methods = ['GET', 'POST'])
def add():
    title = 'Add new album'
    form = AlbumForm()
    if form.validate_on_submit(): #m
        album = Album()
        form.populate_obj(album)
        db.session.add(album)
        db.session.commit()
        flash(f'Album {album.name} added')
        return redirect('/')
    return render_template('form.html', title = title, form = form)

if __name__ == '__main__':
    app.run(debug = True)