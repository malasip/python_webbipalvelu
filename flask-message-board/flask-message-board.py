from datetime import datetime
from flask import Flask, render_template, redirect, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.orm import model_form
from secrets import SystemRandom
from markupsafe import escape
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = SystemRandom.randbytes(SystemRandom, 128)

db = SQLAlchemy(app)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String, nullable = False)
    content = db.Column(db.String, nullable = False)
    timestamp = db.Column(db.DateTime, nullable = False, default = datetime.utcnow())
    modified = db.Column(db.DateTime)
    parent_id = db.Column(db.Integer, db.ForeignKey('message.id'))
    replies = db.relationship('Message')

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String, nullable = False)
    displayname = db.Column(db.String, nullable = False)
    password = db.Column(db.String, nullable = False)
    active = db.Column(db.DateTime)
    messages = db.relationship('Message', backref = db.backref('user', remote_side = [id]))

    def setPassword(self, password):
        self.password = generate_password_hash(password)

    def checkPassword(self, password):
        return check_password_hash(self.password, password)
        

NewMessageForm = model_form(Message, db_session = db.session, base_class = FlaskForm, exclude = ['user_id', 'user', 'replies', 'parent', 'timestamp', 'modified'])
EditMessageForm = model_form(Message, db_session = db.session, base_class = FlaskForm, exclude = ['user_id', 'user', 'replies', 'parent', 'timestamp', 'modified'])
ReplyMessageForm = model_form(Message, db_session = db.session, base_class = FlaskForm, exclude = ['user_id', 'user', 'title', 'replies', 'parent', 'timestamp', 'modified'])

@app.before_first_request
class initDB():
    db.create_all()
    user = User(username = 'Mika', displayname = 'Postaaja', active = datetime.utcnow())
    user.setPassword('kala')
    db.session.add(user)
    db.session.commit()
    message = Message(user_id = user.id, title = 'test', content = 'Test message')
    db.session.add(message)
    db.session.commit()

@app.route('/')
def index():
    title = 'All messages'
    messages = Message.query.filter(Message.parent_id == None).order_by(Message.id.desc()).all()
    return render_template('index.html', title = title, messages = messages)

def unpackMessage(message):
    pass

@app.route('/<int:id>/reply', methods = ['GET', 'POST'])
@app.route('/add', methods = ['GET', 'POST'])
def add(id = None):
    if id:
        form = ReplyMessageForm()
    else:
        form = NewMessageForm()
    if form.validate_on_submit():
        message = Message()
        form.populate_obj(message)
        if id:
            message.parent_id = id
            message.title = f'Re: {Message.query.get_or_404(id).title}'
        db.session.add(message)
        db.session.commit()
        flash('Message posted succesfully')
        return redirect('/')
    title = 'Post a new message'
    return render_template('add_form.html', title = title, form = form)

@app.route('/<int:id>/edit', methods = ['GET', 'POST'])
def edit(id = None):
    message = Message.query.get_or_404(id)
    form = EditMessageForm(obj = message)
    if(form.validate_on_submit()):
        form.populate_obj(message)
        message.modified = datetime.utcnow()
        db.session.commit()
        flash('Message modified succesfully')
        return redirect('/')
    title = f'Editing message "{ message.title }"'
    return render_template('edit_form.html', title = title, form = form, id = id)

@app.route('/<int:id>/delete')
def delete(id = None):
    message = Message.query.get_or_404(id)
    db.session.delete(message)
    db.session.commit()
    flash('Message deleted succesfully')
    return redirect('/')


if __name__ == '__main__':
    app.run(debug = True)