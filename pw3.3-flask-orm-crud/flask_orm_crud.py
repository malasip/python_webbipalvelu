from datetime import datetime
from flask import Flask, render_template, redirect, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.orm import model_form
from secrets import SystemRandom
from markupsafe import escape


app = Flask(__name__)
app.secret_key = SystemRandom.randbytes(SystemRandom, 128)

db = SQLAlchemy(app)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user = db.Column(db.String, nullable = False)
    title = db.Column(db.String, nullable = False)
    content = db.Column(db.String, nullable = False)
    timestamp = db.Column(db.DateTime, nullable = False, default = datetime.utcnow())
    modified = db.Column(db.DateTime)
    parent_id = db.Column(db.Integer, db.ForeignKey('message.id'))
    replies = db.relationship('Message', backref = db.backref('parent', remote_side = [id]))

NewMessageForm = model_form(Message, db_session = db.session, base_class = FlaskForm, exclude = ['replies', 'parent', 'timestamp', 'modified'])
EditMessageForm = model_form(Message, db_session = db.session, base_class = FlaskForm, exclude = ['user', 'replies', 'parent', 'timestamp', 'modified'])
ReplyMessageForm = model_form(Message, db_session = db.session, base_class = FlaskForm, exclude = ['title', 'replies', 'parent', 'timestamp', 'modified'])

@app.before_first_request
class initDB():
    db.create_all()

@app.route('/')
def index():
    title = 'All messages'
    messages = Message.query.filter(Message.parent_id == None).all()
    return render_template('index.html', title = title, messages = messages)

@app.route('/add', methods = ['GET', 'POST'])
def add():
    if not request.args.get('reply'):
        form = NewMessageForm()
    else:
        form = ReplyMessageForm()
    if(form.validate_on_submit()):
        message = Message()
        form.populate_obj(message)
        if request.args.get('reply'):
            parent_id = int(request.args.get('reply'))
            message.parent_id = parent_id
            message.title = f'Re: {Message.query.get(parent_id).title}'
        db.session.add(message)
        db.session.commit()
        flash('Message posted succesfully')
        return redirect('/')
    title = 'Post a new message'
    return render_template('add_form.html', title = title, form = form)

@app.route('/edit', methods = ['GET', 'POST'])
def edit():
    id = escape(request.args.get('id'))
    message = Message.query.get(id)
    form = EditMessageForm(obj = message)
    if(form.validate_on_submit()):
        form.populate_obj(message)
        message.modified = datetime.utcnow()
        db.session.commit()
        flash('Message modified succesfully')
        return redirect('/')
    title = f'Editing message "{ message.title }"'
    return render_template('edit_form.html', title = title, form = form, id = id)

@app.route('/delete')
def delete():
    id = escape(request.args.get('id'))
    message = Message.query.get(id)
    db.session.delete(message)
    db.session.commit()
    flash('Message deleted succesfully')
    return redirect('/')


if __name__ == '__main__':
    app.run(debug = True)