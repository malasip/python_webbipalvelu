from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.orm import model_form
from secrets import SystemRandom



app = Flask(__name__)
app.secret_key = SystemRandom.randbytes(SystemRandom, 128)

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True) 
    email = db.Column(db.String, nullable = False)
    creditcard_no = db.Column(db.String, nullable = False)
    ver_code = db.Column(db.String, nullable = False)

UserForm = model_form(model = User, base_class = FlaskForm, db_session = db.session)

@app.before_first_request
class initDB():
    db.create_all()

@app.route('/')
def index():
    title = 'Index page'
    return render_template('index.html', title = title)

@app.route('/form')
def form():
    title = 'Chekc if your credit card still works'
    form = UserForm()
    return render_template('form.html', title = title, form = form)

if __name__ == '__main__':
    app.run(debug = True)