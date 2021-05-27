from datetime import datetime
from flask import Flask, render_template, redirect, flash, request
from flask_sqlalchemy import SQLAlchemy, model
from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.orm import model_form
from secrets import SystemRandom


app = Flask(__name__)
app.secret_key = SystemRandom.randbytes(SystemRandom, 128)

db = SQLAlchemy(app)

@app.before_first_request
def initDB():
    db.create_all()

class Person(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String, nullable = False)
    last_name = db.Column(db.String, nullable = False)
    phone = db.Column(db.String, nullable = False)
    email = db.Column(db.String, nullable = False)
    address = db.Column(db.String, nullable = False)
    city = db.Column(db.String, nullable = False)
    deleted = db.Column(db.DateTime)

PersonForm = model_form(Person, db_session = db.session, base_class = FlaskForm, exclude = ['deleted'])

@app.route('/')
def index():
    title = 'Directory'
    persons = Person.query.filter(Person.deleted == None).all()
    return render_template('index.html', title = title, persons = persons)

@app.route('/add', methods = ['GET', 'POST'])
@app.route('/<int:id>/edit', methods = ['GET', 'POST'])
def personForm(id = False):
    title = 'Add new contact'
    form = PersonForm()
    if id:
        person = Person.query.get_or_404(id)
        form = PersonForm(obj = person)
        title = f'Modifying contact "{person.first_name} {person.last_name}"'
    if form.validate_on_submit():
        person = Person()
        if id:
            person = Person.query.get_or_404(id)
            form.populate_obj(person)
            flash(f'{person.first_name} {person.last_name} modified')
        else:
            form.populate_obj(person)
            flash(f'{person.first_name} {person.last_name} added')
        db.session.add(person)
        db.session.commit()
        return redirect('/')
    return render_template('form.html', title = title, form = form)

@app.route('/<int:id>/delete')
@app.route('/delete_all')
def deletePerson(id = False):
    if id:
        person = Person.query.get_or_404(id)
        person.deleted = datetime.utcnow()
        flash(f'{person.first_name} {person.last_name} has been deleted')
    else:
        db.session.query(Person).filter(Person.deleted == None).update({Person.deleted: datetime.utcnow()})
        flash('Directory has been emptied')
    db.session.commit()
    return redirect('/')

@app.route('/recover', methods = ['GET', 'POST'])
def recoverPerson():
    title = 'Recover deleted contacts'
    if request.form.getlist('person_checkbox') != []:
        print(request.form.getlist('person_checkbox'))
        for person_id in request.form.getlist('person_checkbox'):
            db.session.query(Person).filter(Person.id == person_id).update({Person.deleted: None})
        db.session.commit()
        flash('Selected contacts have been restored')
        return redirect('/')
    persons = Person.query.filter(Person.deleted != None).all()
    return render_template('recover.html', title = title, persons = persons)
    

if __name__ == '__main__':
    app.run(debug = True)