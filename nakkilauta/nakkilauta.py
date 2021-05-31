from datetime import datetime
from flask import Flask, render_template, redirect, request, flash, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from secrets import token_bytes, token_urlsafe
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import StringField, PasswordField, TextAreaField, validators
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from urllib.parse import urlparse, urljoin
from sqlalchemy import exc


app = Flask(__name__)
app.secret_key = token_bytes(128)
register_token = token_urlsafe(20)

login_manager = LoginManager()
login_manager.init_app(app)

with open('token', 'w') as f:
    f.write(register_token)

db = SQLAlchemy(app)

# User model and functions
class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String, nullable = False, unique = True)
    displayname = db.Column(db.String, nullable = False, unique = True)
    pwhash = db.Column(db.String, nullable = False)
    active = db.Column(db.Boolean, default = False)
    moderator = db.Column(db.Boolean, nullable = False, default = False)
    messages = db.relationship('Message', backref = db.backref('user', remote_side = [id]))

    def is_active(self):
        return True

    def is_authenticated(self):
        return True
    
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    def setPassword(self, password):
        self.pwhash = generate_password_hash(password)

    def checkPassword(self, password):
        return check_password_hash(self.pwhash, password)

# User creation/ edit forms
class UserForm(FlaskForm):
    username = StringField('Username', validators = [validators.InputRequired()])
    password = PasswordField('Password', validators = [validators.InputRequired()])
    displayname = StringField('Display name', validators = [validators.InputRequired()])
    token = StringField('Register token', validators = [validators.InputRequired()])

# User login form
class LoginForm(FlaskForm):
    username = StringField('Username', validators = [validators.InputRequired()])
    password = PasswordField('Password', validators = [validators.InputRequired()])

# User login manager
@login_manager.user_loader
def loadUser(id):
    return User.query.get(id)

@login_manager.unauthorized_handler
def unauthorized():
    title = 'Unauthorized'
    content = 'You need to be logged in to access this page'
    return render_template('40x.html', title = title, content = content)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    title = db.Column(db.String, nullable = False)
    message = db.Column(db.String, nullable = False)
    timestamp = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)
    modified = db.Column(db.DateTime)
    deleted = db.Column(db.DateTime)
    parent_id = db.Column(db.Integer, db.ForeignKey('message.id'))
    replies = db.relationship('Message')

# Message creation forms
class NewMessageForm(FlaskForm):
    title = StringField('Title', validators = [validators.InputRequired()])
    message = TextAreaField('Message', validators = [validators.InputRequired()])

class NoTitleMessageForm(FlaskForm):
    message = TextAreaField('Message', validators = [validators.InputRequired()])

# Initialize database
@app.before_first_request
class initDB():
    db.create_all()
    if User.query.filter(User.username == 'Moderator').first() == None:
        user = User(username = 'Moderator', displayname = 'Moderator', moderator = True)
        user.setPassword('Moderator')
        db.session.add(user)
        db.session.commit()

# Url helper
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

# Error page handlers
@app.errorhandler(400)
def error_page(error):
    print(error)
    title = 'Error loading page'
    content = 'There was an error accessing page. Team of monkeys have been dispatched to reseolve the issue.'
    return render_template('40x.html', title = title, content = content)

@app.errorhandler(404)
def page_not_found():
    title = 'Page not found'
    content = 'The page you tried to access does not exist or was removed'
    return render_template('40x.html', title = title, content = content)

# Application routes

# User endpoints
@app.route('/register', methods = ['GET', 'POST'])
def register():
    form = UserForm()
    if form.validate_on_submit():
        if(form.token.data != register_token):
            flash('Invalid token')
            return redirect('/user/register')
        user = User(username = form.username.data, displayname = form.displayname.data)
        user.setPassword(form.password.data)
        try:
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash('User created successfully.')
        except exc.IntegrityError:
            db.session.rollback()
            flash('Username not avalable')
            return redirect('/user/register')
        return redirect(url_for('index'))
    return render_template('form.html', form = form)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter(User.username == username).first()
        if not user:
            flash('Login failed, bad username or password')
            return redirect(url_for('login'))
        if not user.checkPassword(password):
            flash('Login failed, bad username or password')
            return redirect(url_for('login'))
        login_user(user)
        flash(f'Logged in as {user.displayname}')
        next = request.args.get('next')
        if not is_safe_url(next):
            return abort(400)
        return redirect(next or url_for('index'))
    return render_template('form.html', form = form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully')
    return redirect('/')


# Message endpoints
@app.route('/<int:id>')
@app.route('/')
def index(id = None):
    if id:
        message = Message.query.get_or_404(id)
        if message.deleted:
            flash('That message has been deleted')
            return redirect('/')
        messages = [message]
        return render_template('index.html', messages = messages)
    messages = Message.query.filter(Message.parent_id == None).filter(Message.deleted == None).order_by(Message.id.desc()).all()
    return render_template('index.html', messages = messages)

@app.route('/<int:id>/reply', methods = ['GET', 'POST'])
@app.route('/add', methods = ['GET', 'POST'])
@login_required
def add(id = None):
    if id:
        form = NoTitleMessageForm()
    else:
        form = NewMessageForm()
    if form.validate_on_submit():
        message = Message()
        form.populate_obj(message)
        message.user_id = current_user.get_id()
        if id:
            message.parent_id = id
            message.title = f'Re: {Message.query.get_or_404(id).title}'
        try:
            db.session.add(message)
            db.session.commit()
            flash('Message posted succesfully')
            next = request.args.get('next')
            if not is_safe_url(next):
                return abort(400)
            return redirect(next or url_for('index'))
        except:
            db.session.rollback()
            flash('Something went wrong')
            return abort(400)
    return render_template('form.html', form = form)

@app.route('/<int:id>/edit', methods = ['GET', 'POST'])
@login_required
def edit(id = None):
    message = Message.query.get_or_404(id)
    if message.user_id != current_user.get_id() or not current_user.moderator:
        flash('You do not have permission to modify this message')
        next = request.args.get('next')
        if not is_safe_url(next):
            return abort(400)
        return redirect(next or url_for('index'))
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
        next = request.args.get('next')
        if not is_safe_url(next):
            return abort(400)
        return redirect(next or url_for('index'))
    return render_template('form.html', form = form, id = id)

@app.route('/<int:id>/delete')
@login_required
def delete(id = None):
    message = Message.query.get_or_404(id)
    message.deleted = datetime.utcnow()
    db.session.commit()
    flash('Message deleted succesfully')
    next = request.args.get('next')
    if not is_safe_url(next):
        return abort(400)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug = True)