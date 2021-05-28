from datetime import datetime
from flask import Flask, render_template, redirect, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm, validators
from wtforms.ext.sqlalchemy.orm import model_form
from secrets import SystemRandom
from markupsafe import escape
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, PasswordField, TextAreaField, validators
from sqlalchemy import exc


app = Flask(__name__)
app.secret_key = SystemRandom.randbytes(SystemRandom, 128)

db = SQLAlchemy(app)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String, nullable = False)
    message = db.Column(db.String, nullable = False)
    timestamp = db.Column(db.DateTime, nullable = False, default = datetime.utcnow())
    modified = db.Column(db.DateTime)
    parent_id = db.Column(db.Integer, db.ForeignKey('message.id'))
    replies = db.relationship('Message')

NewMessageForm = model_form(Message, db_session = db.session, base_class = FlaskForm, exclude = ['user_id', 'user', 'replies', 'parent', 'timestamp', 'modified', 'thread_id'])
NoTitleMessageForm = model_form(Message, db_session = db.session, base_class = FlaskForm, exclude = ['user_id', 'user', 'title', 'replies', 'parent', 'timestamp', 'modified', 'thread_id'])
# Message creation/ edit forms
class NewMessageForm(FlaskForm):
    title = StringField('Title', validators = [validators.InputRequired()])
    message = TextAreaField('Message', validators = [validators.InputRequired()])

class NoTitleMessageForm(FlaskForm):
    message = TextAreaField('Message', validators = [validators.InputRequired()])



# User model and functions
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String, nullable = False, unique = True)
    displayname = db.Column(db.String, nullable = False, unique = True)
    pwhash = db.Column(db.String, nullable = False)
    active = db.Column(db.DateTime, default = datetime.utcnow())
    moderator = db.Column(db.Boolean, nullable = False, default = False)
    messages = db.relationship('Message', backref = db.backref('user', remote_side = [id]))

    def setPassword(self, password):
        self.pwhash = generate_password_hash(password)

    def checkPassword(self, password):
        return check_password_hash(self.pwhash, password)

def currentUser():
    try:
        uid = int(session['uid'])
    except:
        return None
    return User.query.get_or_404(uid)

# Set currentUser function as global for Jinja
app.jinja_env.globals['currentUser'] = currentUser

# User login and creation/ edit forms
class UserForm(FlaskForm):
    username = StringField('Username', validators = [validators.InputRequired()])
    password = PasswordField('Password', validators = [validators.InputRequired()])
    displayname = StringField('Display name', validators = [validators.InputRequired()])

class LoginForm(FlaskForm):
    username = StringField('Username', validators = [validators.InputRequired()])
    password = PasswordField('Password', validators = [validators.InputRequired()])

# Initialize database
@app.before_first_request
class initDB():
    db.create_all()
    user = User(username = 'Moderator', displayname = 'Moderator', moderator = True)
    user.setPassword('Moderator')
    db.session.add(user)
    db.session.commit()
    message = Message(user_id = user.id, title = 'First post', message = 'This is a first post')
    db.session.add(message)
    db.session.commit()

@app.route('/user/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter(User.username == username).first()
        if not user:
            flash('Login failed, bad username or password')
            return redirect('/user/login')
        if user.checkPassword(password) and user.active != None:
            session['uid'] = user.id
            flash('Login successfull')
            url = request.args.get('r')
            if not url:
                url = '/'
            return redirect(url)
        flash('Login failed, bad username or password')
        return redirect('/user/login')
    return render_template('form.html', form = form)

@app.route('/user/register', methods = ['GET', 'POST'])
def register():
    form = UserForm()
    if form.validate_on_submit():
        user = User(username = form.username.data, displayname = form.displayname.data)
        user.setPassword(form.password.data)
        try:
            db.session.add(user)
            db.session.commit()
            flash('User created successfully.')
        except exc.IntegrityError:
            db.session.rollback()
            flash('Username not avalable')
            return redirect('/user/register')
        session['uid'] = user.id
        url = request.args.get('r')
        if not url:
            url = '/'
        return redirect(url)
    return render_template('form.html', form = form)

@app.route('/user/logout')
def logout():
    session['uid'] = None
    flash('Logged out successfully')
    return redirect('/')

@app.route('/<int:id>')
@app.route('/')
def index(id = None):
    if id:
        message = Message.query.get_or_404(id)
        messages = [message]
        return render_template('index.html', messages = messages)
    messages = Message.query.filter(Message.parent_id == None).order_by(Message.id.desc()).all()
    return render_template('index.html', messages = messages)

@app.route('/<int:id>/reply', methods = ['GET', 'POST'])
@app.route('/add', methods = ['GET', 'POST'])
def add(id = None):
    if currentUser() == None:
        flash('This action requires valid user')
        return redirect('/')
    if id:
        form = NoTitleMessageForm()
    else:
        form = NewMessageForm()
    if form.validate_on_submit():
        message = Message()
        form.populate_obj(message)
        message.user_id = currentUser().id
        url = '/'
        if id:
            message.parent_id = id
            message.title = f'Re: {Message.query.get_or_404(id).title}'
            url = request.args.get('r')
        try:
            db.session.add(message)
            db.session.commit()
            flash('Message posted succesfully')
            return redirect(url)
        except:
            db.session.rollback()
            flash('Something went wrong')
            return redirect(url)
    return render_template('form.html', form = form)

@app.route('/<int:id>/edit', methods = ['GET', 'POST'])
def edit(id = None):
    if currentUser() == None:
        flash('This action requires valid user')
        return redirect('/')
    message = Message.query.get_or_404(id)
    if message.user_id != currentUser().id or not currentUser().moderator:
        flash('You do not have permission to modify this message')
        return redirect('/')
    form = NoTitleMessageForm(obj = message)
    if(form.validate_on_submit()):
        form.populate_obj(message)
        message.modified = datetime.utcnow()
        try:
            db.session.commit()
            flash('Message modified succesfully')
        except:
            db.session.rollback()
            flash('Something went wrong')
        url = request.args.get('r')
        return redirect(url)
    #title = f'Editing message "{ message.title }"'
    return render_template('form.html', form = form, id = id)

@app.route('/<int:id>/delete')
def delete(id = None):
    if currentUser() == None:
        flash('This action requires valid user')
        return redirect('/')
    message = Message.query.get_or_404(id)
    db.session.delete(message)
    db.session.commit()
    flash('Message deleted succesfully')
    url = request.args.get('r')
    return redirect(url)


if __name__ == '__main__':
    app.run(debug = True)