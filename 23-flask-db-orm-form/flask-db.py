from datetime import datetime
from flask import Flask
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.orm import model_form

app = Flask(__name__)
app.secret_key = 'gufds098ghou4an a9fasgf89afg89aseasf'

db = SQLAlchemy(app)

class Device(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    created = db.Column(db.DateTime, nullable = False, default=datetime.utcnow)
    devtype_id = db.Column(db.Integer, db.ForeignKey('devtype.id'), nullable = False)

class Devtype(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False)
    devices = db.relationship('Device', backref=db.backref('devtype', lazy=True))

DeviceForm = model_form(model = Device, base_class = FlaskForm, db_session = db.session)

@app.before_first_request
def initDB():
    db.create_all()
    db.session.add(Devtype(name = 'Laptop'))
    db.session.add(Devtype(name = 'Desktop'))
    db.session.commit()
    db.session.add(Device(name = 'ProBook 840', devtype = Devtype.query.filter_by(name = 'Laptop').first()))
    db.session.add(Device(name = 'EliteBook Z1', devtype = Devtype.query.filter_by(name = 'Laptop').first()))
    db.session.add(Device(name = 'EliteDesk Z', devtype = Devtype.query.filter_by(name = 'Desktop').first()))
    db.session.commit()

@app.route('/')
def index():
    devices = Device.query.all()
    title = 'Simple database with relations'
    return render_template('index.html', title = title, devices = devices)

@app.route('/add', methods = ['GET', 'POST'])
def add():
    title = 'Add new device'
    form = DeviceForm()
    return render_template('new.html', title = title, form = form)

if __name__ == '__main__':
    app.run(debug=True)