from flask import Flask, render_template, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.orm import model_form
from secrets import SystemRandom

app = Flask(__name__)
app.secret_key = SystemRandom.randbytes(SystemRandom, 128)

db = SQLAlchemy(app)

@app.before_first_request
def initDB():
    db.create_all()

class Game(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)

GameForm = model_form(Game, db_session = db.session, base_class = FlaskForm)

@app.route('/')
def index():
    title = 'Game list'
    games = Game.query.all()
    return render_template('index.html', title = title, games = games)

@app.route('/add-game', methods = ['GET', 'POST'])
def add_game():
    title = 'Add new game'
    form = GameForm()
    if form.validate_on_submit():
        game = Game()
        form.populate_obj(game)
        db.session.add(game)
        db.session.commit()
        flash('Game added')
        return redirect('/')
    return render_template('add.html', title = title, form = form)

if __name__ == '__main__':
    app.run(debug = True)