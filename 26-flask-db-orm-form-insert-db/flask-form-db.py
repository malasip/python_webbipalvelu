from datetime import datetime
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.orm import model_form
from markupsafe import escape
from secrets import SystemRandom

app = Flask(__name__)
app.secret_key = SystemRandom.randbytes(SystemRandom, 128)

db = SQLAlchemy(app)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user = db.Column(db.String, nullable = False)
    created = db.Column(db.DateTime, nullable = False, default=datetime.now)
    parent_id = db.Column(db.Integer, db.ForeignKey('message.id'))
    parent = db.relationship('Message', remote_side=[id])

MessageForm = model_form(model = Message, base_class = FlaskForm, db_session = db.session)

@app.before_first_request
def initDB():
    db.create_all()
    message1 = Message(user = 'Testaaja')
    message2 = Message(user = 'Testaaja2', parent = message1)
    message3 = Message(user = 'Testaaja2', parent = message2)
    db.session.add(message1)
    db.session.add(message2)
    db.session.add(message3)
    db.session.commit()

@app.route('/')
def index():
    messages = Message.query.all()
    for message in messages:
        print(message.parent)
    title = 'Simple messageboard'
    return render_template('index.html', title = title, messages = messages)

@app.route('/add', methods = ['POST'])
def add():
    form = MessageForm()
    message = Message()
    if(request.method == 'POST' and request.form.get('csrf_token') != None):
        # form.populate_obj(device)
        # db.session.add(device)
        # db.session.commit()
        pass
    title = 'Add new device'
    return render_template('add_form.html', title = title, form = form)

if __name__ == '__main__':
    app.run(debug=True)