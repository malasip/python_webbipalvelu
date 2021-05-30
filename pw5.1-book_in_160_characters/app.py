from flask import Flask, render_template, redirect, flash, request, abort, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators
from werkzeug.security import generate_password_hash, check_password_hash
from secrets import SystemRandom
from flask_login import LoginManager, login_user, logout_user, login_required
from urllib.parse import urlparse, urljoin

app = Flask(__name__)
app.secret_key = SystemRandom.randbytes(SystemRandom, 128)

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)

@app.before_first_request
def initDB():
    db.create_all()
    db.session.add(Book(name = 'Harry Potter and the Chamber of Secrets', description = 'The second instalment of boy wizard Harry Potter\'s adventures at Hogwarts School of Witchcraft and Wizardry, based on the novel by JK Rowling'))
    db.session.add(Book(name = 'Harry Potter and the Philosopher\'s Stone', description = 'Harry Potter thinks he is an ordinary boy - until he is rescued by a beetle-eyed giant of a man and enrols at Hogwarts School of Witchcraft and Wizardry.'))
    db.session.commit()

class Book(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    description = db.Column(db.String(160), nullable = False)

class BookForm(FlaskForm):
    name = StringField('Book name', validators = [validators.InputRequired()])
    description = StringField('Book description', validators = [validators.InputRequired(), validators.length(max=160)])

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String, nullable = False)
    pwhash = db.Column(db.String, nullable = False)

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

class UserForm(FlaskForm):
    username = StringField('Username', validators = [validators.InputRequired()])
    password = PasswordField('Password', validators = [validators.InputRequired()])

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

@login_manager.user_loader
def loadUser(id):
    return User.query.get(id)

@login_manager.unauthorized_handler
def unauthorized():
    title = 'Unauthorized'
    content = 'You need to be logged in to access this page'
    return render_template('40x.html', title = title, content = content)

@app.errorhandler(404)
def page_not_found():
    title = 'Page not found'
    content = 'The page you tried to access does not exist or was removed'
    return render_template('40x.html', title = title, content = content)

@app.route('/register', methods = ['GET', 'POST'])
def register():
    form = UserForm()
    if form.validate_on_submit():
        user = User()
        user.username = form.username.data
        user.setPassword(form.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('Registered succesfully')
        next = request.args.get('next')
        if not is_safe_url(next):
            return abort(400)
        return redirect(next or url_for('index'))
    return render_template('form.html', form = form)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = UserForm()
    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user.checkPassword(form.password.data):
            login_user(user)
            flash('Logged in succesfully')
            next = request.args.get('next')
            if not is_safe_url(next):
                return abort(400)
        return redirect(next or url_for('index'))
    return render_template('form.html', form = form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/')
@app.route('/<int:id>')
def index(id = None):
    if id:
        books = [Book.query.get_or_404(id)]
    else:
        books = Book.query.all()
    return render_template('index.html', books = books)

@app.route('/add', methods = ['GET', 'POST'])
@app.route('/<int:id>/edit', methods = ['GET', 'POST'])
@login_required
def bookForm(id = None):
    form = BookForm()
    book = Book()
    if id:
        book = Book.query.get_or_404(id)
        form = BookForm(obj = book)
    if form.validate_on_submit():
        form.populate_obj(book)
        try:
            db.session.add(book)
            db.session.commit()
            flash(f'{ book.name} added succesfully')
            return redirect('/')
        except:
            db.session.rollback()
            flash(f'{ book.name} could not be added')
            return redirect('/')

    return render_template('/form.html', form = form)

@app.route('/<int:id>/delete')
@login_required
def deleteBook(id = None):
    if id:
        book = Book.query.get_or_404(id)
        try:
            db.session.delete(book)
            db.session.commit()
            flash(f'{ book.name } has been deleted')
            return redirect('/')
        except:
            db.session.rollback()
        return redirect('/')
    flash('No id supplied or invalid id')
    return redirect('/')



if __name__ == '__main__':
    app.run(debug = True)