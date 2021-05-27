from flask import Flask, render_template, redirect, flash
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from wtforms.ext.sqlalchemy.orm import model_form
from secrets import SystemRandom

app = Flask(__name__)
app.secret_key = SystemRandom.randbytes(SystemRandom, 128)

db = SQLAlchemy(app)

@app.before_first_request
def initDB():
    db.create_all()

class Book(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    author = db.Column(db.String, nullable = False)

BookForm = model_form(Book, db_session = db.session, base_class = FlaskForm)

@app.route('/')
def index():
    title = 'Simple book database'
    books = Book.query.all()
    return render_template('index.html', title = title, books = books)

@app.route('/add', methods = ['GET', 'POST'])
def add():
    title = 'Add new book'
    form = BookForm()
    if form.validate_on_submit(): #m
        book = Book()
        form.populate_obj(book)
        db.session.add(book)
        db.session.commit()
        flash(f'Book {book.name} added')
        return redirect('/')
    return render_template('add.html', title = title, form = form)

if __name__ == '__main__':
    app.run(debug = True)