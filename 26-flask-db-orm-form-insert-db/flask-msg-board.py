from datetime import datetime
from flask import Flask, render_template, request, redirect
from flask.helpers import flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from sqlalchemy.orm import backref
from wtforms.ext.sqlalchemy.orm import model_form
from markupsafe import escape
from secrets import SystemRandom

from wtforms.fields.core import IntegerField, StringField
from wtforms.fields.simple import HiddenField

app = Flask(__name__)
app.secret_key = SystemRandom.randbytes(SystemRandom, 128)

db = SQLAlchemy(app)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user = db.Column(db.String, nullable = False)
    message = db.Column(db.String, nullable = False)
    created = db.Column(db.DateTime, nullable = False, default = datetime.now)
    deleted = db.Column(db.Boolean, nullable = False, default = False)
    parent_id = db.Column(db.Integer, db.ForeignKey('message.id'))
    children = db.relationship('Message', backref = db.backref('parent', remote_side = [id]))

class NewMessageForm(FlaskForm):
    user = StringField('User')
    message = StringField('Message')

#MessageForm = model_form(model = Message, base_class = NewMessageForm, db_session = db.session)

@app.before_first_request
def initDB():
    db.create_all()
    message1 = Message(user = 'Testaaja', message = 'Test message 1')
    message2 = Message(user = 'Testaaja2', message = 'Test message 2', parent = message1)
    message3 = Message(user = 'Testaaja2', message = 'Test message 3', parent = message1)
    db.session.add(message1)
    db.session.add(message2)
    db.session.add(message3)
    db.session.commit()

@app.route('/')
def index():
    messages = Message.query.filter(Message.deleted == False).all()
    print(messages)
    title = 'Simple messageboard'
    return render_template('index.html', title = title, messages = messages)

@app.route('/add', methods = ['GET', 'POST'])
def add():
    form = NewMessageForm()
    message = Message()
    if(request.method == 'POST' and request.form.get('csrf_token') != None):
        form.populate_obj(message)
        db.session.add(message)
        db.session.commit()
        flash('Message posted succesfully')
        return redirect('/')
    title = 'Add new message'
    return render_template('add_form.html', title = title, form = form)

@app.route('/reply/<int:id>', methods = ['GET', 'POST'])
def reply(id):
    form = NewMessageForm()
    message = Message()
    message.parent_id = id
    if(request.method == 'POST' and request.form.get('csrf_token') != None):
        form.populate_obj(message)
        db.session.add(message)
        db.session.commit()
        flash('Message posted succesfully')
        return redirect('/')
    title = 'Reply to message'
    return render_template('add_form.html', title = title, form = form)

@app.route('/delete/<int:id>', methods = ['GET'])
def delete(id):
    message = Message.query.get(id)
    message.deleted = True
    print(id)
    db.session.commit()
    flash('Message deleted')
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)